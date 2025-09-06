from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import ServiceRecord, MaintenanceRecord, Technician
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from datetime import datetime
from .forms import MaintenanceUpdateForm
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from django.utils import timezone
from notifications.views import create_notification


# Create your views here.

def is_aftersales(user):
    return user.groups.filter(name='Aftersales').exists()

@login_required
@user_passes_test(is_aftersales)
def aftersales_base(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'aftersales/aftersales_base.html', {'profile': profile})

@login_required
@user_passes_test(is_aftersales)
def aftersales_dashboard(request):
    # Get maintenance records with related service records and sales orders
    maintenance_records = MaintenanceRecord.objects.select_related(
        'service_record',
        'service_record__sales_order'
    ).all().order_by('-created_at')
    
    # For each maintenance record, get the service record and its sales order
    for maintenance in maintenance_records:
        try:
            service = ServiceRecord.objects.select_related('sales_order').get(service_id=maintenance.service_id)
            maintenance.service = service
        except ServiceRecord.DoesNotExist:
            maintenance.service = None
    
    all_technicians = Technician.objects.all()
    warranty_actives = ServiceRecord.objects.filter(status='Warranty Active').count()
    now = timezone.now()
    resolved_this_month = sum(1 for m in maintenance_records if m.status == 'Completed')
    maintenance_in_progress = sum(1 for m in maintenance_records if m.status == 'In Progress')
    context = {
        'maintenance_records': maintenance_records,
        'all_technicians': all_technicians,
        'warranty_actives': warranty_actives,
        'resolved_this_month': resolved_this_month,
        'maintenance_in_progress': maintenance_in_progress,
    }
    return render(request, 'pages/aftersales_dashboard.html', context)

@login_required
@user_passes_test(is_aftersales)
def aftersales_received_requests(request):
    return render(request, 'pages/internal_requests/aftersales_received_requests.html')

@login_required
@user_passes_test(is_aftersales)
def aftersales_sent_requests(request):
    return render(request, 'pages/internal_requests/aftersales_sent_requests.html')

@login_required
@user_passes_test(is_aftersales)
def aftersales_maintenance_schedule(request):
    # Get maintenance records with related service records and sales orders
    maintenance_records = MaintenanceRecord.objects.select_related(
        'service_record',
        'service_record__sales_order'
    ).all().order_by('-created_at')
    
    # For each maintenance record, get the service record and its sales order
    for maintenance in maintenance_records:
        try:
            service = ServiceRecord.objects.select_related('sales_order').get(service_id=maintenance.service_id)
            maintenance.service = service
            # Debug print
            print(f"Maintenance ID: {maintenance.maintenance_id}")
            print(f"Service ID: {service.service_id}")
            print(f"Sales Order: {service.sales_order.order_number if service.sales_order else 'None'}")
        except ServiceRecord.DoesNotExist:
            maintenance.service = None
            print(f"No service record found for maintenance ID: {maintenance.maintenance_id}")
    
    all_technicians = Technician.objects.all()
    context = {
        'maintenance_records': maintenance_records,
        'all_technicians': all_technicians,
    }
    return render(request, 'pages/aftersales_maintenance_schedule.html', context)

@login_required
@user_passes_test(is_aftersales)
def aftersales_logs(request):
    # Get all service records with their completed maintenance records
    service_records = ServiceRecord.objects.prefetch_related(
        models.Prefetch(
            'maintenance_records',
            queryset=MaintenanceRecord.objects.filter(status='Completed'),
            to_attr='completed_maintenance_records'
        )
    ).all()
    
    # Add has_maintenance flag to each service record (True if any maintenance record is not completed/cancelled)
    for record in service_records:
        record.has_maintenance = record.maintenance_records.exclude(status__in=['Completed', 'Cancelled']).exists()
        # Add service record to each maintenance record
        if hasattr(record, 'completed_maintenance_records'):
            for maintenance in record.completed_maintenance_records:
                maintenance.service = record
    
    # Get all technicians for the modals
    all_technicians = Technician.objects.all()
    
    context = {
        'service_records': service_records,
        'all_technicians': all_technicians,
    }
    
    return render(request, 'pages/aftersales_logs.html', context)


@login_required
@user_passes_test(is_aftersales)
def aftersales_logs_feed(request):
    """Return latest service records for logs page as JSON for AJAX polling."""
    service_records = ServiceRecord.objects.all().order_by('-created_at')[:200]
    results = []
    for rec in service_records:
        results.append({
            'service_id': rec.service_id,
            'unit_name': rec.unit_name,
            'serial_number': rec.serial_number,
            'client_name': rec.client_name,
            'warranty_type': rec.warranty_type,
            'warranty_start': rec.warranty_start.strftime('%Y-%m-%d') if rec.warranty_start else '',
            'warranty_end': rec.warranty_end.strftime('%Y-%m-%d') if rec.warranty_end else '',
            'status': rec.status,
        })
    return JsonResponse({'records': results})

@login_required
@user_passes_test(is_aftersales)
def aftersales_settings(request):
    # Get or create user settings
    from adminpanel.models import UserSettings
    user_settings, created = UserSettings.objects.get_or_create(
        user=request.user,
        defaults={
            'timezone': 'UTC+08:00',  # Default to Manila timezone
            'date_format': 'MM/DD/YYYY'
        }
    )

    if request.method == 'POST':
        if 'save_settings' in request.POST:
            timezone = request.POST.get('timezone')
            date_format = request.POST.get('dateFormat')

            if timezone:
                user_settings.timezone = timezone
            if date_format:
                user_settings.date_format = date_format

            user_settings.save()
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Settings saved successfully!')
            return redirect('aftersales_settings')

    timezone_choices = [
        ('UTC-12:00', '(UTC-12:00) International Date Line West'),
        ('UTC-11:00', '(UTC-11:00) Coordinated Universal Time-11'),
        ('UTC-10:00', '(UTC-10:00) Hawaii'),
        ('UTC-09:00', '(UTC-09:00) Alaska'),
        ('UTC-08:00', '(UTC-08:00) Pacific Time (US & Canada)'),
        ('UTC-07:00', '(UTC-07:00) Mountain Time (US & Canada)'),
        ('UTC-06:00', '(UTC-06:00) Central Time (US & Canada)'),
        ('UTC-05:00', '(UTC-05:00) Eastern Time (US & Canada)'),
        ('UTC-04:00', '(UTC-04:00) Atlantic Time (Canada)'),
        ('UTC-03:00', '(UTC-03:00) Buenos Aires'),
        ('UTC-02:00', '(UTC-02:00) Mid-Atlantic'),
        ('UTC-01:00', '(UTC-01:00) Azores'),
        ('UTC+00:00', '(UTC+00:00) London, Lisbon, Casablanca'),
        ('UTC+01:00', '(UTC+01:00) Berlin, Paris, Madrid, Rome'),
        ('UTC+02:00', '(UTC+02:00) Athens, Cairo, Johannesburg'),
        ('UTC+03:00', '(UTC+03:00) Moscow, Riyadh, Nairobi'),
        ('UTC+04:00', '(UTC+04:00) Dubai, Baku, Muscat'),
        ('UTC+05:00', '(UTC+05:00) Islamabad, Karachi'),
        ('UTC+05:30', '(UTC+05:30) India Standard Time (IST)'),
        ('UTC+06:00', '(UTC+06:00) Dhaka, Astana'),
        ('UTC+07:00', '(UTC+07:00) Bangkok, Jakarta, Hanoi'),
        ('UTC+08:00', '(UTC+08:00) Beijing, Singapore, Manila'),
        ('UTC+09:00', '(UTC+09:00) Tokyo, Seoul'),
        ('UTC+09:30', '(UTC+09:30) Adelaide, Darwin'),
        ('UTC+10:00', '(UTC+10:00) Sydney, Brisbane'),
        ('UTC+11:00', '(UTC+11:00) Solomon Islands, New Caledonia'),
        ('UTC+12:00', '(UTC+12:00) Auckland, Fiji'),
    ]

    date_format_choices = [
        ('MM/DD/YYYY', 'MM/DD/YYYY (e.g. 05/02/2025)'),
        ('DD/MM/YYYY', 'DD/MM/YYYY (e.g. 02/05/2025)'),
        ('YYYY-MM-DD', 'YYYY-MM-DD (e.g. 2025-05-02)'),
        ('MMM DD, YYYY', 'MMM DD, YYYY (e.g. May 02, 2025)'),
    ]

    context = {
        'user_settings': user_settings,
        'timezone_choices': timezone_choices,
        'date_format_choices': date_format_choices,
    }

    return render(request, 'pages/aftersales_settings.html', context)

@require_http_methods(["POST"])
def create_maintenance(request):
    try:
        data = json.loads(request.body)
        print("Received data:", data)  # Debug log
        
        # Validate required fields
        required_fields = ['service_id', 'unit_name', 'serial_number', 'client_name']
        for field in required_fields:
            if field not in data or not data[field]:
                return JsonResponse({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }, status=400)
        
        # Get the service record
        try:
            service = ServiceRecord.objects.get(service_id=data['service_id'])
        except ServiceRecord.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Service record not found'
            }, status=404)
        
        # Only block if there is an active (not completed/cancelled) maintenance record
        if MaintenanceRecord.objects.filter(service_record=service).exclude(status__in=['Completed', 'Cancelled']).exists():
            return JsonResponse({
                'success': False,
                'error': 'There is already an active maintenance record for this service'
            }, status=400)
        
        # Generate maintenance ID (MTN-YY-XXXX)
        year = datetime.now().strftime('%y')
        last_maintenance = MaintenanceRecord.objects.order_by('-maintenance_id').first()
        if last_maintenance:
            last_number = int(last_maintenance.maintenance_id.split('-')[-1])
            new_number = str(last_number + 1).zfill(4)
        else:
            new_number = '0001'
        
        maintenance_id = f'MTN-{year}-{new_number}'
        print("Generated maintenance_id:", maintenance_id)  # Debug log
        
        # Create new maintenance record
        maintenance = MaintenanceRecord.objects.create(
            maintenance_id=maintenance_id,
            service_record=service,
            service_id=service.service_id,
            unit_name=data['unit_name'],
            serial_number=data['serial_number'],
            client_name=data['client_name'],
            status='Pending'  # Default status
        )
        
        # Create notification for admin panel
        create_notification(
            title='New Maintenance Request',
            message=f'New maintenance request {maintenance_id} has been created for {data["client_name"]}',
            notification_type='new_maintenance_request',
            from_dept='aftersales',
            to_dept='admin',
            related_id=None,
            related_link=f'/adminpanel/aftersales/?maintenance_id={maintenance_id}'
        )
        
        print("Created maintenance record:", maintenance.maintenance_id)  # Debug log
        
        return JsonResponse({
            'success': True,
            'maintenance_id': maintenance.maintenance_id,
            'redirect_url': '/aftersales/maintenance_schedule/'
        })
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        print("Error creating maintenance record:", str(e))  # Debug log
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
@user_passes_test(is_aftersales)
def update_maintenance(request, maintenance_id):
    maintenance = get_object_or_404(MaintenanceRecord, maintenance_id=maintenance_id)
    if request.method == 'POST':
        form = MaintenanceUpdateForm(request.POST, instance=maintenance)
        if form.is_valid():
            instance = form.save(commit=False)
            tech_names = request.POST.getlist('technicians')
            # Check if all fields are filled
            all_filled = (
                bool(instance.reported_problem and instance.diagnosis and instance.findings_note and instance.work_performed)
                and any(name.strip() for name in tech_names)
            )
            if all_filled:
                instance.status = 'Completed'
            elif instance.reported_problem or tech_names:
                instance.status = 'In Progress'
            instance.save()
            # Handle multiple technicians from POST
            tech_objs = []
            for name in tech_names:
                name = name.strip()
                if name:
                    tech, _ = Technician.objects.get_or_create(name=name)
                    tech_objs.append(tech)
            instance.technicians.set(tech_objs)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = MaintenanceUpdateForm(instance=maintenance)
        all_technicians = Technician.objects.all()
    return render(request, 'aftersales_modals/maintenance_schedule_modals/view_schedule_modal.html', {'form': form, 'maintenance': maintenance, 'all_technicians': all_technicians})

