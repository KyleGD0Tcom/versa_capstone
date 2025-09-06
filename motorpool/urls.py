from django.urls import path
from . import views

urlpatterns = [
    path('base/', views.motorpool_base, name='motorpool_base'),
    path('dashboard/', views.motorpool_dashboard, name='motorpool_dashboard'),
    path('received_requests/', views.motorpool_received_requests, name='motorpool_received_requests'),
    path('received_requests/feed/', views.motorpool_received_requests_feed, name='motorpool_received_requests_feed'),
    path('sent_requests/', views.motorpool_sent_requests, name='motorpool_sent_requests'),
    path('equipment_inspection/', views.motorpool_equipment_inspection, name='motorpool_equipment_inspection'),
    path('settings/', views.motorpool_settings, name='motorpool_settings'),
    path('update-request-notes/', views.update_request_notes, name='update_request_notes'),
    path('update-request-status/', views.update_request_status, name='update_request_status'),
    path('update-inspection/', views.update_inspection, name='update_inspection'),
    path('send-to-delivery/', views.send_to_delivery, name='send_to_delivery'),
    path('check-delivery-exists/', views.check_delivery_exists, name='check_delivery_exists'),
]
