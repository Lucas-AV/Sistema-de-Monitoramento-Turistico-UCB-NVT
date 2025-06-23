
from django.db import models
from django.utils import timezone # Importar para usar timezone.now
from django.contrib.auth.models import User # Importar o modelo de usuário padrão do Django

class PontoTuristico(models.Model):
    """
    Modelo para representar um Ponto Turístico.
    Contém informações como nome, localização e tipo.
    """
    nome = models.CharField(max_length=255, verbose_name="Nome do Ponto Turístico")
    localizacao = models.CharField(max_length=255, verbose_name="Localização")
    tipo = models.CharField(max_length=100, verbose_name="Tipo de Ponto Turístico",
                            help_text="Ex: Monumento, Parque, Museu, Praia, etc.")

    class Meta:
        verbose_name = "Ponto Turístico"
        verbose_name_plural = "Pontos Turísticos"

    def __str__(self):
        return self.nome

class Turista(models.Model):
    """
    Modelo para representar um Turista.
    Contém informações sobre o nome, país/estado de origem e o tipo (nacional/internacional).
    """
    NACIONAL = 'Nacional'
    INTERNACIONAL = 'Internacional'
    TIPO_CHOICES = [
        (NACIONAL, 'Nacional'),
        (INTERNACIONAL, 'Internacional'),
    ]

    nome = models.CharField(max_length=255, verbose_name="Nome do Turista", blank=True, null=True)
    pais_estado_origem = models.CharField(max_length=255, verbose_name="País/Estado de Origem")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default=NACIONAL,
                            verbose_name="Tipo de Turista")

    class Meta:
        verbose_name = "Turista"
        verbose_name_plural = "Turistas"

    def __str__(self):
        if self.nome:
            return f"{self.nome} ({self.pais_estado_origem} - {self.tipo})"
        return f"{self.pais_estado_origem} ({self.tipo})"

class Visita(models.Model):
    """
    Modelo para registrar uma Visita a um Ponto Turístico.
    Registra o ponto visitado, o horário da visita e a origem do turista.
    """
    ponto_visitado = models.ForeignKey(PontoTuristico, on_delete=models.CASCADE,
                                       related_name='visitas', verbose_name="Ponto Visitado")
    turista = models.ForeignKey(Turista, on_delete=models.CASCADE,
                                related_name='visitas', verbose_name="Turista")
    horario = models.DateTimeField(verbose_name="Horário da Visita", default=timezone.now)
    origem_turista_str = models.CharField(max_length=255, blank=True, null=True,
                                        verbose_name="Origem do Turista (String para relatórios)")

    class Meta:
        verbose_name = "Visita"
        verbose_name_plural = "Visitas"
        ordering = ['-horario']

    def __str__(self):
        return f"Visita de {self.turista} em {self.ponto_visitado.nome} ({self.horario.strftime('%Y-%m-%d %H:%M')})"

    def save(self, *args, **kwargs):
        if not self.origem_turista_str:
            self.origem_turista_str = f"{self.turista.pais_estado_origem} ({self.turista.tipo})"
            if self.turista.nome:
                self.origem_turista_str = f"{self.turista.nome} - {self.origem_turista_str}"
        super().save(*args, **kwargs)

class NotificationMessage(models.Model):
    """
    Modelo para armazenar mensagens de notificação para usuários.
    Permite persistir notificações e marcá-las como dispensadas.
    """
    INFO = 'info'
    SUCCESS = 'success'
    WARNING = 'warning'
    ERROR = 'error'
    TYPE_CHOICES = [
        (INFO, 'Informativa'),
        (SUCCESS, 'Sucesso'),
        (WARNING, 'Aviso'),
        (ERROR, 'Erro'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name="Usuário")
    message = models.TextField(verbose_name="Mensagem")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=INFO, verbose_name="Tipo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criada em")
    is_dismissed = models.BooleanField(default=False, verbose_name="Dispensada")
    notification_id_hash = models.CharField(max_length=64, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.type.upper()}] para {self.user.username}: {self.message[:50]}..."


