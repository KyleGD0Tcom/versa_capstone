from django.urls import path
from . import views

urlpatterns = [
    path('', views.delivery_base, name='delivery_base'),
    path('dashboard/', views.delivery_dashboard, name='delivery_dashboard'),
    path('requests/', views.delivery_requests, name='delivery_requests'),
    path('requests/feed/', views.delivery_requests_feed, name='delivery_requests_feed'),
    path('tracker/', views.delivery_tracker, name='delivery_tracker'),
    path('logs/', views.delivery_logs, name='delivery_logs'),
    path('internal_requests/', views.delivery_internal_requests, name='delivery_internal_requests'),
    path('settings/', views.delivery_settings, name='delivery_settings'),
    path('api/create-schedule/', views.create_delivery_schedule, name='create_delivery_schedule'),
    path('api/update-status/', views.update_delivery_status, name='update_delivery_status'),
]
