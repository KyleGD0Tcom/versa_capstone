from django.urls import path
from . import views

app_name = 'notifications'
 
urlpatterns = [
    path('get/', views.get_notifications, name='get_notifications'),
    path('feed/', views.get_notifications_feed, name='get_notifications_feed'),
    path('mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('center/', views.notification_center, name='notification_center'),
] 