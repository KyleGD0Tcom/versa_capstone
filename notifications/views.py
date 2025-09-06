from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import Notification
from django.contrib.auth.models import Group

# Create your views here.

@login_required
def get_notifications(request):
    # Get user's department
    user_department = request.user.groups.first().name.lower() if request.user.groups.exists() else None
    
    if not user_department:
        return JsonResponse({'notifications': []})
    
    # Get unread notifications for user's department
    notifications = Notification.objects.filter(
        to_department=user_department
    ).exclude(
        read_by=request.user
    ).order_by('-created_at')[:5]  # Get last 5 unread notifications
    
    notifications_data = [{
        'id': notif.id,
        'title': notif.title,
        'message': notif.message,
        'notification_type': notif.notification_type,
        'from_department': notif.from_department,
        'created_at': notif.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'related_link': notif.related_link,
        'is_read': request.user in notif.read_by.all()
    } for notif in notifications]
    
    return JsonResponse({
        'notifications': notifications_data,
        'unread_count': notifications.count()
    })

@login_required
def get_notifications_feed(request):
    """Return latest notifications for real-time updates as JSON for AJAX polling."""
    # Get user's department
    user_department = request.user.groups.first().name.lower() if request.user.groups.exists() else None
    
    if not user_department:
        return JsonResponse({'notifications': []})
    
    # Get recent notifications for user's department (last 10)
    notifications = Notification.objects.filter(
        to_department=user_department
    ).order_by('-created_at')[:10]
    
    notifications_data = [{
        'id': notif.id,
        'title': notif.title,
        'message': notif.message,
        'notification_type': notif.notification_type,
        'from_department': notif.from_department,
        'created_at': notif.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'related_link': notif.related_link,
        'is_read': request.user in notif.read_by.all()
    } for notif in notifications]
    
    return JsonResponse({
        'notifications': notifications_data,
        'unread_count': notifications.exclude(read_by=request.user).count()
    })

@login_required
def mark_notification_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.mark_as_read(request.user)
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Notification not found'}, status=404)

@login_required
def notification_center(request):
    user_department = request.user.groups.first().name.lower() if request.user.groups.exists() else None
    
    if not user_department:
        return render(request, 'notifications/notification_center.html', {'notifications': []})
    
    notifications = Notification.objects.filter(
        to_department=user_department
    ).order_by('-created_at')
    
    # Map department to base template
    department_templates = {
        'motorpool': 'motorpool/motorpool_base.html',
        'delivery': 'delivery/delivery_base.html',
        'sales': 'sales/sales_base.html',
        'warehouse': 'warehouse/warehouse_base.html',
        'aftersales': 'aftersales/aftersales_base.html',
        'admin': 'adminpanel/base.html'
    }
    
    # Get the appropriate base template
    base_template = department_templates.get(user_department, 'delivery/delivery_base.html')
    
    return render(request, 'notifications/notification_center.html', {
        'notifications': notifications,
        'base_template': base_template
    })

def create_notification(title, message, notification_type, from_dept, to_dept, related_id=None, related_link=None):
    """
    Utility function to create a new notification
    Can be imported and used by other apps
    """
    notification = Notification.objects.create(
        title=title,
        message=message,
        notification_type=notification_type,
        from_department=from_dept,
        to_department=to_dept,
        related_id=related_id,
        related_link=related_link
    )
    return notification
