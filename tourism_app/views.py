
from django.shortcuts import render, redirect
from django.db.models import Count, Avg
from django.db.models.functions import TruncDate
import matplotlib.pyplot as plt
import io
import urllib.parse
import base64
import plotly.express as px
import json
from datetime import datetime, timedelta, date
import numpy as np
from .models import PontoTuristico, Turista, Visita, NotificationMessage
from django.http import HttpResponse
import csv
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
import hashlib

# Encoder JSON personalizado para lidar com tipos não serializáveis padrão
class DjangoPlotlyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

@login_required
def dashboard_view(request):
    """
    View para exibir o dashboard principal do sistema com filtros de data e gráficos.
    Carrega dados para os contadores e gera gráficos para visualização.
    """
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    today = datetime.now().date()
    default_start_date = today - timedelta(days=30)
    default_end_date = today

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else default_start_date
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else default_end_date
    except ValueError:
        start_date = default_start_date
        end_date = default_end_date

    filtered_visitas = Visita.objects.filter(
        horario__date__gte=start_date,
        horario__date__lte=end_date
    )

    total_pontos = PontoTuristico.objects.count()
    total_visitas = filtered_visitas.count()
    visitas_nacionais = filtered_visitas.filter(turista__tipo=Turista.NACIONAL).count()
    visitas_internacionais = filtered_visitas.filter(turista__tipo=Turista.INTERNACIONAL).count()

    # --- Lógica de Notificação (RF08) ---
    current_notifications_for_display = []
    
    num_days = (end_date - start_date).days + 1
    if num_days <= 0: num_days = 1

    daily_counts_filtered = filtered_visitas.annotate(day=TruncDate('horario')).values('day').annotate(count=Count('id'))
    avg_visits_filtered = daily_counts_filtered.aggregate(avg_count=Avg('count'))['avg_count'] or 0

    last_7_days_visitas = Visita.objects.filter(
        horario__date__gte=today - timedelta(days=7),
        horario__date__lte=today
    ).annotate(day=TruncDate('horario')).values('day').annotate(count=Count('id'))
    last_7_days_avg = last_7_days_visitas.aggregate(avg_count=Avg('count'))['avg_count'] or 0
    
    base_avg_for_comparison = avg_visits_filtered if avg_visits_filtered > 0 else last_7_days_avg

    SPIKE_THRESHOLD_FACTOR = 1.5
    DROP_THRESHOLD_FACTOR = 0.5

    notifications_to_save = []
    
    if base_avg_for_comparison > 0:
        if total_visitas > (base_avg_for_comparison * num_days * SPIKE_THRESHOLD_FACTOR):
            message = f'Pico de visitação detectado! Total de visitas ({total_visitas}) no período é significativamente alto (média diária: {avg_visits_filtered:.2f}).'
            notifications_to_save.append({'type': NotificationMessage.SUCCESS, 'message': message})
        elif total_visitas > 0 and total_visitas < (base_avg_for_comparison * num_days * DROP_THRESHOLD_FACTOR):
            message = f'Queda de visitação detectada! Total de visitas ({total_visitas}) no período é significativamente baixo (média diária: {avg_visits_filtered:.2f}).'
            notifications_to_save.append({'type': NotificationMessage.WARNING, 'message': message})
    
    if total_visitas == 0 and num_days > 0:
        message = f'Nenhuma visita registrada no período de {num_days} dias selecionado.'
        notifications_to_save.append({'type': NotificationMessage.INFO, 'message': message})
    elif total_visitas > 0 and base_avg_for_comparison == 0:
        message = f'Há {total_visitas} visitas registradas, mas não há média de comparação histórica para o período.'
        notifications_to_save.append({'type': NotificationMessage.INFO, 'message': message})
    elif total_visitas == 0 and base_avg_for_comparison == 0:
        message = 'Sem dados de visitação para gerar notificações de tendência.'
        notifications_to_save.append({'type': NotificationMessage.INFO, 'message': message})

    for notif_data in notifications_to_save:
        notif_hash = hashlib.sha256(f"{notif_data['message']}-{notif_data['type']}-{today.strftime('%Y-%m-%d')}".encode()).hexdigest()
        
        existing_notif = NotificationMessage.objects.filter(
            user=request.user,
            notification_id_hash=notif_hash,
            created_at__date=today
        ).first()

        if not existing_notif:
            NotificationMessage.objects.create(
                user=request.user,
                message=notif_data['message'],
                type=notif_data['type'],
                notification_id_hash=notif_hash,
                is_dismissed=False
            )
        
        active_notifications = NotificationMessage.objects.filter(
            user=request.user,
            is_dismissed=False,
            created_at__date=today
        ).order_by('-created_at')

    current_notifications_for_display = list(active_notifications.values('id', 'message', 'type', 'notification_id_hash'))


    # --- Geração de Gráfico Matplotlib (Visitas por Tipo de Turista) ---
    data_by_type = filtered_visitas.values('turista__tipo').annotate(count=Count('id')).order_by('turista__tipo')
    types = [d['turista__tipo'] for d in data_by_type]
    counts = [int(d['count']) for d in data_by_type]

    matplotlib_graph_uri = None
    if types and counts and sum(counts) > 0:
        plt.figure(figsize=(8, 5))
        plt.bar(types, counts, color=['skyblue', 'lightcoral'])
        plt.title('Visitas por Tipo de Turista (Filtrado)')
        plt.xlabel('Tipo de Turista')
        plt.ylabel('Número de Visitas')
        plt.grid(axis='y', linestyle='--')

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        matplotlib_graph_uri = urllib.parse.quote(base64.b64encode(buf.read()).decode('utf-8'))

    # --- Geração de Gráfico Plotly (Visitas por Ponto Turístico) ---
    data_by_point = filtered_visitas.values('ponto_visitado__nome').annotate(count=Count('id')).order_by('-count')

    if data_by_point:
        df_points_data = {
            'Ponto Turístico': [d['ponto_visitado__nome'] for d in data_by_point],
            'Número de Visitas': [int(d['count']) for d in data_by_point]
        }
        fig_points = px.bar(df_points_data, x='Ponto Turístico', y='Número de Visitas',
                            title='Visitas por Ponto Turístico (Filtrado)',
                            labels={'Ponto Turístico': 'Ponto Turístico', 'Número de Visitas': 'Total de Visitas'})
        plotly_graph_json = json.dumps(fig_points.to_dict(), cls=DjangoPlotlyJSONEncoder)
    else:
        plotly_graph_json = json.dumps({"data": [], "layout": {"title": "Sem dados de visitas por ponto turístico para o período"}})

    # --- Geração de Gráfico Plotly (Análise Temporal de Visitas) ---
    temporal_data = filtered_visitas.annotate(day=TruncDate('horario')).values('day').annotate(count=Count('id')).order_by('day')

    if temporal_data:
        df_temporal_data = {
            'Data': [d['day'].strftime('%Y-%m-%d') for d in temporal_data],
            'Número de Visitas': [int(d['count']) for d in temporal_data]
        }
        fig_temporal = px.line(df_temporal_data, x='Data', y='Número de Visitas',
                               title='Análise Temporal de Visitas (Filtrado)',
                               labels={'Data': 'Data', 'Número de Visitas': 'Total de Visitas Diárias'})
        plotly_temporal_graph_json = json.dumps(fig_temporal.to_dict(), cls=DjangoPlotlyJSONEncoder)
    else:
        plotly_temporal_graph_json = json.dumps({"data": [], "layout": {"title": "Sem dados temporais para o período"}})


    context = {
        'total_pontos': total_pontos,
        'total_visitas': total_visitas,
        'visitas_nacionais': visitas_nacionais,
        'visitas_internacionais': visitas_internacionais,
        'matplotlib_graph_uri': matplotlib_graph_uri,
        'plotly_graph_json': plotly_graph_json,
        'plotly_temporal_graph_json': plotly_temporal_graph_json,
        'start_date_input': start_date.strftime('%Y-%m-%d'),
        'end_date_input': end_date.strftime('%Y-%m-%d'),
        'notifications': current_notifications_for_display,
    }
    return render(request, 'tourism_app/dashboard.html', context)


@login_required
def reports_view(request):
    """
    View para exibir a página de relatórios detalhados.
    Permite visualizar e filtrar visitas.
    """
    all_visits = Visita.objects.select_related('ponto_visitado', 'turista').order_by('-horario')

    ponto_turistico_id = request.GET.get('ponto_turistico')
    tipo_turista = request.GET.get('tipo_turista')
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if ponto_turistico_id:
        all_visits = all_visits.filter(ponto_visitado__id=ponto_turistico_id)
    if tipo_turista:
        all_visits = all_visits.filter(turista__tipo=tipo_turista)
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            all_visits = all_visits.filter(horario__date__gte=start_date)
        except ValueError:
            pass
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            all_visits = all_visits.filter(horario__date__lte=end_date)
        except ValueError:
            pass


    pontos_turisticos = PontoTuristico.objects.all().order_by('nome')

    context = {
        'visits': all_visits,
        'pontos_turisticos': pontos_turisticos,
        'tipos_turista': Turista.TIPO_CHOICES,
        'current_ponto_turistico': ponto_turistico_id,
        'current_tipo_turista': tipo_turista,
        'current_start_date': start_date_str,
        'current_end_date': end_date_str,
    }
    return render(request, 'tourism_app/reports.html', context)

@login_required
def export_visits_csv(request):
    """
    View para exportar os dados de visitas como um arquivo CSV.
    Permite aplicar os mesmos filtros da página de relatórios.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="relatorio_visitas.csv"'

    writer = csv.writer(response)
    writer.writerow(['Ponto Turístico', 'Localização', 'Tipo Ponto', 'Nome Turista', 'Origem Turista', 'Tipo Turista', 'Horário da Visita'])

    visits_to_export = Visita.objects.select_related('ponto_visitado', 'turista').order_by('-horario')

    ponto_turistico_id = request.GET.get('ponto_turistico')
    tipo_turista = request.GET.get('tipo_turista')
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if ponto_turistico_id:
        visits_to_export = visits_to_export.filter(ponto_visitado__id=ponto_turistico_id)
    if tipo_turista:
        visits_to_export = visits_to_export.filter(turista__tipo=tipo_turista)
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            visits_to_export = visits_to_export.filter(horario__date__gte=start_date)
        except ValueError:
            pass
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            visits_to_export = visits_to_export.filter(horario__date__lte=end_date)
        except ValueError:
            pass

    for visit in visits_to_export:
        writer.writerow([
            visit.ponto_visitado.nome,
            visit.ponto_visitado.localizacao,
            visit.ponto_visitado.tipo,
            visit.turista.nome if visit.turista.nome else 'N/A',
            visit.turista.pais_estado_origem,
            visit.turista.tipo,
            visit.horario.strftime('%Y-%m-%d %H:%M:%S')
        ])

    return response


def register_view(request):
    """
    View para o registro de novos usuários.
    Utiliza o formulário de criação de usuário padrão do Django.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def notifications_history_view(request):
    """
    View para exibir o histórico de notificações do usuário logado.
    Permite visualizar notificações ativas e dispensadas.
    """
    user_notifications = NotificationMessage.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'notifications': user_notifications,
    }
    return render(request, 'tourism_app/notifications_history.html', context)


