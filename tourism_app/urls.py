
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('reports/', views.reports_view, name='reports'),
    path('reports/export-csv/', views.export_visits_csv, name='export_visits_csv'),

    path('accounts/register/', views.register_view, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('notifications-history/', views.notifications_history_view, name='notifications_history'),
]


