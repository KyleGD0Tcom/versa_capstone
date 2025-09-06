from django.urls import path
from . import views

urlpatterns = [
    path('/', views.aftersales_base, name='aftersales_base'),
    path('dashboard/', views.aftersales_dashboard, name='aftersales_dashboard'),
    path('received_requests/', views.aftersales_received_requests, name='aftersales_received_requests'),
    path('sent_requests/', views.aftersales_sent_requests, name='aftersales_sent_requests'),
    path('maintenance_schedule/', views.aftersales_maintenance_schedule, name='aftersales_maintenance_schedule'),
    path('logs/', views.aftersales_logs, name='aftersales_logs'),
    path('logs/feed/', views.aftersales_logs_feed, name='aftersales_logs_feed'),
    path('settings/', views.aftersales_settings, name='aftersales_settings'),
    path('create_maintenance/', views.create_maintenance, name='create_maintenance'),
    path('maintenance/update/<str:maintenance_id>/', views.update_maintenance, name='update_maintenance'),
]

