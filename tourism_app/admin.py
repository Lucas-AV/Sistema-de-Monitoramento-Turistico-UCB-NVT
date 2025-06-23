
from django.contrib import admin
from .models import PontoTuristico, Turista, Visita, NotificationMessage

# Registra os modelos para que sejam visíveis e gerenciáveis no painel administrativo do Django
admin.site.register(PontoTuristico)
admin.site.register(Turista)
admin.site.register(Visita)
admin.site.register(NotificationMessage)


