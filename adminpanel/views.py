from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . models import UserProfile, UserSettings
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.db import connection
from django.urls import reverse
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from sales.models import Invoice, SalesOrder, Request, RequestNote
from warehouse.models import WarehouseInvoice, WarehouseOrder
from aftersales.models import MaintenanceRecord, ServiceRecord
from django.views.decorators.http import require_http_methods
import json

# Create your views here.

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

@login_required
@user_passes_test(is_admin)
def admin_base(request):
    return render(request, 'adminpanel/base.html')


@login_required
@user_passes_test(is_admin)
def dashboard_view(request):
    return render(request, 'pages/dashboard.html')



@login_required
@user_passes_test(is_admin)
def Operations_inventory_view(request):
    # Handle form submission
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the item to the database
            messages.success(request, 'Item added successfully!')
            return redirect(request.path_info)  # Redirect to the same URL
    else:
        form = InventoryItemForm()  # For GET requests, show the empty form
    
    # Fetch all inventory items to display in the table
    inventory_items = InventoryItem.objects.all()

    # Calculate dashboard metrics
    # Total items in stock by department
    warehouse_total = inventory_items.filter(department='Warehouse').aggregate(total=Sum('quantity'))['total'] or 0
    sales_total = inventory_items.filter(department='Sales').aggregate(total=Sum('quantity'))['total'] or 0

    # Low stock items (quantity < 20) by department
    warehouse_low_stock = inventory_items.filter(department='Warehouse', quantity__lt=20).count()
    sales_low_stock = inventory_items.filter(department='Sales', quantity__lt=20).count()

    # New items added this week by department
    one_week_ago = timezone.now().date() - timedelta(days=7)
    warehouse_new_items = inventory_items.filter(department='Warehouse', date_received__gte=one_week_ago).count()
    sales_new_items = inventory_items.filter(department='Sales', date_received__gte=one_week_ago).count()

    return render(request, 'pages/Operations/inventory.html', {
        'form': form,
        'inventory_items': inventory_items,
        'warehouse_total': warehouse_total,
        'sales_total': sales_total,
        'warehouse_low_stock': warehouse_low_stock,
        'sales_low_stock': sales_low_stock,
        'warehouse_new_items': warehouse_new_items,
        'sales_new_items': sales_new_items
    })



@login_required
@user_passes_test(is_admin)
def Operations_forecast_view(request):
    return render(request, 'pages/Operations/forecast.html')


@login_required
@user_passes_test(is_admin)
def motorpool_view(request):
    from sales.models import Request
    from django.utils import timezone
    now = timezone.now()

    # Pending PDI Requests
    pending_pdi_requests = Request.objects.filter(
        request_type='PDI',
        assigned_to='Motorpool',
        status='Pending'
    ).count()

    # Repairs in Progress
    repairs_in_progress = Request.objects.filter(
        request_type='PDI',
        assigned_to='Motorpool',
        status='In Progress'
    ).count()

    # Completed Inspections (count all with status Completed)
    completed_inspections = Request.objects.filter(
        request_type='PDI',
        assigned_to='Motorpool',
        status='Completed'
    ).count()

    # All sales requests for the table
    sales_requests = list(Request.objects.filter(
        request_type='PDI',
        assigned_to='Motorpool'
    ).order_by('-created_at'))

    # Attach invoice object to each request (Sales or Warehouse)
    from sales.models import Invoice
    from warehouse.models import WarehouseInvoice
    invoice_numbers = [req.invoice_number for req in sales_requests if req.invoice_number]
    sales_invoices = {inv.invoice_number: inv for inv in Invoice.objects.filter(invoice_number__in=invoice_numbers)}
    warehouse_invoices = {inv.invoice_number: inv for inv in WarehouseInvoice.objects.filter(invoice_number__in=invoice_numbers)}
    for req in sales_requests:
        req.invoice = sales_invoices.get(req.invoice_number) or warehouse_invoices.get(req.invoice_number)

    context = {
        'pending_pdi_requests': pending_pdi_requests,
        'repairs_in_progress': repairs_in_progress,
        'completed_inspections': completed_inspections,
        'sales_requests': sales_requests,
    }
    return render(request, 'pages/Operations/motorpool.html', context)



@login_required
@user_passes_test(is_admin)
def SalesAndOrders_view(request):
    # Get current month's start and end dates
    today = timezone.now()
    first_day_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # Get all orders for this month from both departments
    monthly_sales_orders = SalesOrder.objects.filter(
        order_date__gte=first_day_of_month,
        order_date__lte=last_day_of_month
    )
    monthly_warehouse_orders = WarehouseOrder.objects.filter(
        order_date__gte=first_day_of_month,
        order_date__lte=last_day_of_month
    )

    # Calculate total monthly sales (count of completed orders from both departments)
    total_monthly_sales = (
        monthly_sales_orders.filter(status='Completed').count() +
        monthly_warehouse_orders.filter(status='Completed').count()
    )

    # Get pending orders count from both departments
    pending_orders = (
        SalesOrder.objects.filter(status='Pending').count() +
        WarehouseOrder.objects.filter(status='Pending').count()
    )

    # Get total orders count from both departments
    total_orders = (
        SalesOrder.objects.count() +
        WarehouseOrder.objects.count()
    )

    # Get cancelled orders count from both departments
    cancelled_orders = (
        SalesOrder.objects.filter(status='Cancelled').count() +
        WarehouseOrder.objects.filter(status='Cancelled').count()
    )

    # Get all orders for the table from both departments
    sales_orders = SalesOrder.objects.all().order_by('-order_date')
    warehouse_orders = WarehouseOrder.objects.all().order_by('-order_date')
    
    # Combine and sort all orders
    all_orders = list(sales_orders) + list(warehouse_orders)
    all_orders.sort(key=lambda x: x.order_date, reverse=True)

    context = {
        'total_monthly_sales': total_monthly_sales,
        'pending_orders': pending_orders,
        'total_orders': total_orders,
        'cancelled_orders': cancelled_orders,
        'orders': all_orders,
    }

    return render(request, 'pages/Operations/sales_and_orders.html', context)


@login_required
@user_passes_test(is_admin)
def orders_feed(request):
    """Return latest orders data as JSON for AJAX polling."""
    from django.utils import timezone
    
    # Get all orders from both departments
    sales_orders = SalesOrder.objects.all().order_by('-order_date')
    warehouse_orders = WarehouseOrder.objects.all().order_by('-order_date')
    
    # Combine and sort all orders
    all_orders = list(sales_orders) + list(warehouse_orders)
    all_orders.sort(key=lambda x: x.order_date, reverse=True)
    
    results = []
    for order in all_orders:
        # Determine order type and get appropriate data
        if hasattr(order, 'item_description'):  # SalesOrder
            item_description = order.item_description
            order_type = 'SalesOrder'
        else:  # WarehouseOrder
            if order.items.all():
                item_description = ', '.join([f"{item.quantity}x {item.inventory_item.unit_item}" for item in order.items.all()])
            else:
                item_description = '-'
            order_type = 'WarehouseOrder'
        
        results.append({
            'id': order.id,
            'order_number': order.order_number,
            'client_name': order.client_name,
            'item_description': item_description,
            'total_amount': str(order.total_amount),
            'order_date': order.order_date.isoformat(),
            'delivery_date': order.delivery_date.isoformat(),
            'status': order.status,
            'order_type': order_type,
            'created_at': order.order_date.isoformat(),
        })
    
    return JsonResponse({'orders': results})



@login_required
@user_passes_test(is_admin)
def Operations_invoicing_view(request):
    # Get current month's start and end dates
    today = timezone.now()
    first_day_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # Get all invoices for this month
    sales_invoices = Invoice.objects.filter(
        invoice_date__gte=first_day_of_month,
        invoice_date__lte=last_day_of_month
    )
    warehouse_invoices = WarehouseInvoice.objects.filter(
        invoice_date__gte=first_day_of_month,
        invoice_date__lte=last_day_of_month
    )

    # Calculate total invoices
    total_invoices = sales_invoices.count() + warehouse_invoices.count()

    # Calculate paid invoices
    paid_invoices = (
        sales_invoices.filter(status='Paid').count() +
        warehouse_invoices.filter(status='Paid').count()
    )

    # Calculate pending invoices
    pending_invoices = (
        sales_invoices.filter(status='Pending').count() +
        warehouse_invoices.filter(status='Pending').count()
    )

    # Calculate overdue invoices
    overdue_invoices = (
        sales_invoices.filter(status='Overdue').count() +
        warehouse_invoices.filter(status='Overdue').count()
    )

    # Get all invoices for the table
    all_invoices = list(sales_invoices) + list(warehouse_invoices)
    all_invoices.sort(key=lambda x: x.invoice_date, reverse=True)

    context = {
        'total_invoices': total_invoices,
        'paid_invoices': paid_invoices,
        'pending_invoices': pending_invoices,
        'overdue_invoices': overdue_invoices,
        'invoices': all_invoices,
    }

    return render(request, 'pages/Operations/invoicing.html', context)



@login_required
@user_passes_test(is_admin)
def Aftersales_view(request):
    # Get all maintenance records
    maintenance_records = MaintenanceRecord.objects.all().order_by('-created_at')
    # Attach related ServiceRecord to each maintenance record for modal display
    for maintenance in maintenance_records:
        try:
            service = ServiceRecord.objects.select_related('sales_order').get(service_id=maintenance.service_id)
            maintenance.service = service
        except ServiceRecord.DoesNotExist:
            maintenance.service = None
    # Count all completed records (regardless of date)
    resolved_this_month = maintenance_records.filter(status='Completed').count()
    # In progress
    maintenance_in_progress = maintenance_records.filter(status='In Progress').count()
    # Warranty active
    warranty_actives = ServiceRecord.objects.filter(status='Warranty Active').count()

    context = {
        'maintenance_in_progress': maintenance_in_progress,
        'resolved_this_month': resolved_this_month,
        'warranty_actives': warranty_actives,
        'maintenance_records': maintenance_records,
    }
    return render(request, 'pages/Operations/aftersales.html', context)



@login_required
@user_passes_test(is_admin)
def Delivery_Tracking_view(request):
    from django.utils import timezone
    from delivery.models import DeliverySchedule
    from sales.models import Invoice
    
    # Get today's date
    today = timezone.now().date()
    
    # Get deliveries for today
    deliveries_today = DeliverySchedule.objects.filter(
        delivery_date=today
    ).count()
    
    # Get in-transit deliveries
    in_transit = DeliverySchedule.objects.filter(
        status='In-Transit'
    ).count()
    
    # Get delivered deliveries
    delivered = DeliverySchedule.objects.filter(
        status='Delivered'
    ).count()
    
    # Get failed/returned deliveries
    failed_returned = DeliverySchedule.objects.filter(
        status='Cancelled'
    ).count()
    
    # Get all delivery schedules for the table
    delivery_schedules = DeliverySchedule.objects.select_related(
        'delivery_request'
    ).all().order_by('-delivery_date')
    
    # Fetch related invoices
    for schedule in delivery_schedules:
        try:
            invoice = Invoice.objects.select_related('order').prefetch_related(
                'order__items',
                'order__items__inventory_item'
            ).get(invoice_number=schedule.delivery_request.invoice_number)
            schedule.delivery_request.invoice = invoice  # Attach invoice for template access
            if invoice.order:
                items = invoice.order.items.all()
                schedule.first_item = items.first() if items else None
            else:
                schedule.first_item = None
        except Invoice.DoesNotExist:
            schedule.first_item = None
        except Exception as e:
            schedule.first_item = None
    
    context = {
        'deliveries_today': deliveries_today,
        'in_transit': in_transit,
        'delivered': delivered,
        'failed_returned': failed_returned,
        'delivery_schedules': delivery_schedules,
    }
    
    return render(request, 'pages/deliveryTracking.html', context)

@login_required
@user_passes_test(is_admin)
def RiskAndAnomalies_view(request):
    return render(request, 'pages/risk_and_anomalies.html')


@login_required
@user_passes_test(is_admin)
def AuditTrail_view(request):
    return render(request, 'pages/audit_trail.html')

@login_required
@user_passes_test(is_admin)
def Settings_view(request):
    # Get or create user settings
    user_settings, created = UserSettings.objects.get_or_create(
        user=request.user,
        defaults={
            'timezone': 'UTC+08:00',  # Default to Manila timezone
            'date_format': 'MM/DD/YYYY'
        }
    )
    
    if request.method == 'POST':
        # Handle contact support form
        if 'contact_support' in request.POST:
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            
            # Here you can add logic to send email or save to database
            messages.success(request, 'Support request submitted successfully!')
            return redirect('settings')
        
        # Handle settings form
        elif 'save_settings' in request.POST:
            timezone = request.POST.get('timezone')
            date_format = request.POST.get('dateFormat')
            
            if timezone:
                user_settings.timezone = timezone
            if date_format:
                user_settings.date_format = date_format
            
            user_settings.save()
            messages.success(request, 'Settings saved successfully!')
            return redirect('settings')
    
    # Get available timezone and date format choices
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
    
    return render(request, 'pages/settings.html', context)

@login_required
@user_passes_test(is_admin)
def Notifications_view(request):
    return render(request, 'pages/notifications.html')







from .forms import InventoryItemForm
from .forms import InventoryItem

@login_required
@user_passes_test(is_admin)
def user_management_view(request):
    # Gather statistics for the template (total users and department users)
    total_users = User.objects.filter(is_superuser=False).count()

    # Get number of users per department
    warehouse_users = UserProfile.objects.filter(department='Warehouse').count()    
    motorpool_users = UserProfile.objects.filter(department='Motorpool').count()
    aftersales_users = UserProfile.objects.filter(department='Aftersales').count()
    delivery_users = UserProfile.objects.filter(department='Delivery').count()
    sales_users = UserProfile.objects.filter(department='Sales').count()
    # Prepare context for statistics
    user_management_context = {
        'total_users': total_users,
        'warehouse_users': warehouse_users,
        'motorpool_users': motorpool_users,
        'aftersales_users': aftersales_users,
        'delivery_users': delivery_users,
        'sales_users' : sales_users,
    }


    #CRUD
    if request.method == 'POST':
        # Handle 'Add User' functionality
        if 'add_user' in request.POST:
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            gender = request.POST.get('gender')
            dob = request.POST.get('dob')
            email = request.POST.get('email')
            mobile_number = request.POST.get('mobile_number')
            password = request.POST.get('password')
            department = request.POST.get('department')
            role = request.POST.get('role')
            work_shift = request.POST.get('work_shift')
            status = request.POST.get('status')
            employee_type = request.POST.get('employee_type')
            profile_picture = request.FILES.get('profile_picture')

            # Create User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_active=True
            )

            # Assign the user to the department group
            try:
                group = Group.objects.get(name=department)
                user.groups.add(group)
            except Group.DoesNotExist:
                pass  # Handle group not existing if needed

            # Create UserProfile
            UserProfile.objects.create(
                user=user,
                gender=gender,
                dob=dob,
                mobile_number=mobile_number,
                department=department,
                role=role,
                work_shift=work_shift,
                status=status,
                employee_type=employee_type,
                plain_password=password,
                profile_picture=profile_picture
            )

            messages.success(request, 'User successfully added.')
            return redirect(f"{reverse('user_management')}?success=added")
        
        # Handle 'Update User' functionality
        elif 'update_user' in request.POST:
            user_id = request.POST.get('user_id')  # This is passed to identify which user to update
            user = get_object_or_404(User, id=user_id)
            user_profile = get_object_or_404(UserProfile, user=user)

            # Update User details
            user.username = request.POST.get('username')
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')

            group_name = request.POST.get('department')
            if group_name:
                group = get_object_or_404(Group, name=group_name)
                user.groups.set([group])

            # Only update password if provided
            new_password = request.POST.get('password')
            if new_password is not None:
                user.set_password(new_password)
                user.save()

            user.is_active = True 

            # Update UserProfile details
            user_profile.gender = request.POST.get('gender')
            user_profile.dob = request.POST.get('dob')
            user_profile.mobile_number = request.POST.get('mobile_number')
            user_profile.department = request.POST.get('department')
            user_profile.role = request.POST.get('role')
            user_profile.work_shift = request.POST.get('work_shift')
            user_profile.status = request.POST.get('status')
            user_profile.employee_type = request.POST.get('employee_type')
            user_profile.plain_password = request.POST.get('password')
            
            # Handle profile picture update
            profile_picture = request.FILES.get('profile_picture')
            if profile_picture:
                user_profile.profile_picture = profile_picture
            
            user_profile.save()

            messages.success(request, 'User successfully updated.')
            return redirect(f"{reverse('user_management')}?success=updated")
        

        elif 'delete_user' in request.POST:
            user_id = request.POST.get('user_id')  # Get the user ID from the form
            try:
                user = User.objects.get(id=user_id)  # Fetch the user by ID 
                user.delete()  # Delete the user

                # Reset the auto-increment value for the next user
                with connection.cursor() as cursor:
                    cursor.execute("ALTER TABLE auth_user AUTO_INCREMENT = 2")  # Reset the ID value to 2

                return redirect('user_management')

            except User.DoesNotExist:
                messages.error(request, 'User not found.')
                return JsonResponse({'success': False})  # Return failure


    # If GET request, or after form submission, get all users and groups for rendering
    groups = Group.objects.exclude(name='Admin').exclude(name='Accounts')  # exclude 'Accounts' if needed
    users = User.objects.filter(is_superuser=False)

    user_management_context.update({
        'users': users,
        'groups': groups,
    })
    return render(request, 'pages/user_management.html', user_management_context)








@login_required
@user_passes_test(is_admin)
def department_view(request):
    # Get all departments excluding Admin and Accounts
    departments = Group.objects.exclude(name='Admin').exclude(name='Accounts')
    total_departments = departments.count()
    

    # Dictionary to store department name and user list
    department_data = []

    for dept in departments:
        # Get all UserProfiles where the department matches
        users_in_dept = UserProfile.objects.filter(department=dept.name)

    
        department_data.append({
            'name': dept.name,
            'user_count': users_in_dept.count(),
            'users': users_in_dept,  # Include the list of UserProfile objects
        })

    return render(request, 'pages/department.html', {
        'departments': department_data,
        'total_departments': total_departments,
    })

@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def admin_update_request_notes(request):
    try:
        data = json.loads(request.body)
        request_id = data.get('request_id')
        note_text = data.get('note')
        
        if not note_text:
            return JsonResponse({
                'status': 'error',
                'message': 'Note cannot be empty'
            }, status=400)
        
        # Get the request object
        req = Request.objects.get(id=request_id)
        
        # Create new note
        RequestNote.objects.create(
            request=req,
            note=note_text,
            created_by=request.user
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Note added successfully'
        })
    except Request.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Request not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
