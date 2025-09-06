from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.utils import timezone
import json
from .models import DeliveryRequest, DeliverySchedule
from sales.models import Invoice, SalesOrder
from adminpanel.models import UserProfile, InventoryItem
from warehouse.models import WarehouseInvoice, WarehouseOrder, WarehouseClientRecord
from notifications.views import create_notification
from django.contrib import messages


# Create your views here.

def is_delivery(user):
    return user.groups.filter(name='Delivery').exists()

@login_required
@user_passes_test(is_delivery)
def delivery_base(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'delivery/delivery_base.html', {'profile': profile})

@login_required
@user_passes_test(is_delivery)
def delivery_dashboard(request):
    try:
        # Get today's date
        today = timezone.now().date()
        print(f"\n=== Delivery Dashboard Debug ===")
        print(f"Today's date: {today}")
        
        # Check for unscheduled delivery requests
        unscheduled_requests = DeliveryRequest.objects.filter(status='Pending')
        print(f"\nUnscheduled delivery requests: {unscheduled_requests.count()}")
        for delivery_request in unscheduled_requests:
            print(f"- Request ID: {delivery_request.request_id}")
            print(f"  Invoice: {delivery_request.invoice_number}")
            print(f"  Created: {delivery_request.created_at}")
            print("---")
        
        # Get ALL delivery schedules regardless of date
        all_schedules = DeliverySchedule.objects.all()
        print(f"\nTotal delivery schedules in database: {all_schedules.count()}")
        
        # Show all schedules for debugging
        print("\nAll delivery schedules:")
        for schedule in all_schedules:
            print(f"- ID: {schedule.schedule_id}")
            print(f"  Date: {schedule.delivery_date}")
            print(f"  Status: {schedule.status}")
            print(f"  Created: {schedule.created_at}")
            print("---")
        
        # Count scheduled and in-transit deliveries for today only
        scheduled_deliveries = DeliverySchedule.objects.filter(
            status__in=['Scheduled', 'In-Transit'],
            delivery_date=today
        )
        print(f"\nScheduled Deliveries Query (today only):")
        print(f"SQL: {scheduled_deliveries.query}")
        print(f"Count: {scheduled_deliveries.count()}")
        
        # Count ALL completed deliveries (regardless of date)
        completed_deliveries = DeliverySchedule.objects.filter(
            status='Delivered'
        )
        print(f"\nCompleted Deliveries Query:")
        print(f"SQL: {completed_deliveries.query}")
        print(f"Count: {completed_deliveries.count()}")
        
        # Count ALL cancelled deliveries (regardless of date)
        cancelled_deliveries = DeliverySchedule.objects.filter(
            status='Cancelled'
        )
        print(f"\nCancelled Deliveries Query:")
        print(f"SQL: {cancelled_deliveries.query}")
        print(f"Count: {cancelled_deliveries.count()}")
        
        # Get all unique status values in the database
        all_statuses = DeliverySchedule.objects.values_list('status', flat=True).distinct()
        print(f"\nAll unique status values in database: {list(all_statuses)}")
        
        # Create context with explicit integer values
        scheduled_count = scheduled_deliveries.count()
        completed_count = completed_deliveries.count()
        cancelled_count = cancelled_deliveries.count()
        
        print(f"\nCounts before context:")
        print(f"Scheduled: {scheduled_count}")
        print(f"Completed: {completed_count}")
        print(f"Cancelled: {cancelled_count}")
        
        in_transit_deliveries = DeliverySchedule.objects.filter(status='In-Transit').count()
        context = {
            'in_transit_deliveries': in_transit_deliveries,
            'completed_deliveries': completed_count,
            'returned_deliveries': cancelled_count,
        }
        
        print(f"\nContext being sent to template: {context}")
        print("=== End Debug ===\n")
        
        return render(request, 'pages/delivery_dashboard.html', context)
        
    except Exception as e:
        print(f"Unexpected error in delivery_dashboard: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        # Return a basic context with zeros in case of error
        return render(request, 'pages/delivery_dashboard.html', {
            'in_transit_deliveries': 0,
            'completed_deliveries': 0,
            'returned_deliveries': 0,
        })


@login_required
@user_passes_test(is_delivery)
def delivery_requests(request):
    delivery_requests = DeliveryRequest.objects.all().order_by('-created_at')
    
    # Get invoice and order data for each request
    for delivery_request in delivery_requests:
        try:
            delivery_request.invoice = Invoice.objects.select_related('order').prefetch_related(
                'order__items',
                'order__items__inventory_item'
            ).get(invoice_number=delivery_request.invoice_number)
        except Invoice.DoesNotExist:
            delivery_request.invoice = None

        # Initialize delivery date and instructions
        delivery_request.delivery_date_value = ''
        delivery_request.delivery_instructions_value = ''

        # For sales records (non-warehouse)
        if not delivery_request.invoice_number.startswith('INVWH-'):
            if getattr(delivery_request, 'invoice', None) and getattr(delivery_request.invoice, 'order', None):
                order = delivery_request.invoice.order
                delivery_request.delivery_date_value = order.delivery_date.strftime('%Y-%m-%d') if order.delivery_date else ''
                delivery_request.delivery_instructions_value = order.delivery_instructions or ''
        # For warehouse records
        else:
            if hasattr(delivery_request, 'unit_info'):
                delivery_request.delivery_date_value = delivery_request.unit_info.get('delivery_date', '')
                delivery_request.delivery_instructions_value = delivery_request.unit_info.get('delivery_instructions', '')
    
    return render(request, 'pages/delivery_requests.html', {
        'delivery_requests': delivery_requests
    })


@login_required
@user_passes_test(is_delivery)
def delivery_requests_feed(request):
    """Return latest delivery requests as JSON for AJAX polling."""
    requests_qs = DeliveryRequest.objects.all().order_by('-created_at')[:100]
    results = []
    for dr in requests_qs:
        results.append({
            'id': dr.id,
            'request_id': dr.request_id,
            'invoice_number': dr.invoice_number,
            'unit_name': (dr.unit_info or {}).get('unit_name', ''),
            'serial_number': (dr.unit_info or {}).get('serial_number', ''),
            'client_name': (dr.client_info or {}).get('client_name', ''),
            'status': dr.status,
            'created_at': dr.created_at.isoformat(),
        })
    return JsonResponse({'requests': results})


@login_required
@user_passes_test(is_delivery)
def delivery_tracker(request):
    # Get all delivery schedules with their related data
    delivery_schedules = DeliverySchedule.objects.select_related(
        'delivery_request'
    ).all().order_by('-created_at')
    
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
    
    return render(request, 'pages/delivery_tracker.html', {
        'delivery_schedules': delivery_schedules
    })




@login_required
@user_passes_test(is_delivery)
def delivery_logs(request):
    # Get all delivery schedules with status 'Delivered'
    delivered_schedules = DeliverySchedule.objects.select_related(
        'delivery_request'
    ).filter(
        status='Delivered'
    ).order_by('-delivery_date')  # Most recent deliveries first
    
    # Fetch related invoices and orders
    for schedule in delivered_schedules:
        try:
            # Try sales invoice first
            invoice = Invoice.objects.select_related('order').get(
                invoice_number=schedule.delivery_request.invoice_number
            )
            if invoice and hasattr(invoice, 'order') and invoice.order:
                schedule.order_id = invoice.order.order_number
            else:
                schedule.order_id = ""
        except Invoice.DoesNotExist:
            # Try warehouse invoice if sales invoice not found
            try:
                warehouse_invoice = WarehouseInvoice.objects.select_related('order').get(
                    invoice_number=schedule.delivery_request.invoice_number
                )
                if warehouse_invoice and hasattr(warehouse_invoice, 'order') and warehouse_invoice.order:
                    schedule.order_id = warehouse_invoice.order.order_number
                else:
                    schedule.order_id = ""
            except WarehouseInvoice.DoesNotExist:
                schedule.order_id = ""
        except Exception as e:
            print(f"Error processing schedule {schedule.schedule_id}: {str(e)}")
            schedule.order_id = ""
    
    context = {
        'delivered_schedules': delivered_schedules,
    }
    return render(request, 'pages/delivery_logs.html', context)


@login_required
@user_passes_test(is_delivery)
def delivery_internal_requests(request):
    return render(request, 'pages/delivery_internal_requests.html')


@login_required
@user_passes_test(is_delivery)
def delivery_settings(request):
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
        # Handle settings form
        if 'save_settings' in request.POST:
            timezone = request.POST.get('timezone')
            date_format = request.POST.get('dateFormat')
            
            if timezone:
                user_settings.timezone = timezone
            if date_format:
                user_settings.date_format = date_format
            
            user_settings.save()
            messages.success(request, 'Settings saved successfully!')
            return redirect('delivery_settings')
    
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
    
    return render(request, 'pages/delivery_settings.html', context)


@login_required
@user_passes_test(is_delivery)
@require_POST
def create_delivery_schedule(request):
    try:
        data = json.loads(request.body)
        print("Received data:", data)  # Debug log
        
        # Validate required fields
        required_fields = ['request_id', 'assigned_driver', 'delivery_date']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'status': 'error',
                    'message': f'Missing required field: {field}'
                }, status=400)
        
        # Get the delivery request
        try:
            delivery_request = DeliveryRequest.objects.get(request_id=data['request_id'])
        except DeliveryRequest.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': f'Delivery request not found: {data["request_id"]}'
            }, status=404)
        
        # Check if a schedule already exists
        if DeliverySchedule.objects.filter(delivery_request=delivery_request).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'A delivery schedule already exists for this request.'
            }, status=400)
        
        # Create the schedule
        try:
            schedule = DeliverySchedule.objects.create(
                delivery_request=delivery_request,
                assigned_driver=data['assigned_driver'],
                delivery_date=data['delivery_date'],
                delivery_instructions=data.get('delivery_instructions', '')
            )
            
            # Update the delivery request status
            delivery_request.status = 'Processing'
            delivery_request.save()
            
            # Create notification for admin panel
            create_notification(
                title='New Delivery Schedule Created',
                message=f'New delivery schedule {schedule.schedule_id} has been created for {delivery_request.client_info.get("client_name")}',
                notification_type='new_delivery_schedule',
                from_dept='delivery',
                to_dept='admin',
                related_id=schedule.id,
                related_link=f'/adminpanel/delivery&Tracking/?schedule_id={schedule.schedule_id}'
            )
            
            print("Schedule created:", schedule.schedule_id)  # Debug log
            
            return JsonResponse({
                'status': 'success',
                'message': 'Delivery schedule created successfully.',
                'schedule_id': schedule.schedule_id
            })
        except Exception as e:
            print("Error creating schedule:", str(e))  # Debug log
            return JsonResponse({
                'status': 'error',
                'message': f'Error creating schedule: {str(e)}'
            }, status=500)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        print("Unexpected error:", str(e))  # Debug log
        return JsonResponse({
            'status': 'error',
            'message': f'Unexpected error: {str(e)}'
        }, status=500)


@login_required
@user_passes_test(is_delivery)
@require_POST
def update_delivery_status(request):
    try:
        data = json.loads(request.body)
        schedule_id = data.get('schedule_id')
        new_status = data.get('status')
        
        print(f"\n=== Starting delivery status update ===")
        print(f"Schedule ID: {schedule_id}")
        print(f"New Status: {new_status}")
        
        # Validate required fields
        if not schedule_id or not new_status:
            return JsonResponse({
                'status': 'error',
                'message': 'Missing required fields'
            }, status=400)
        
        # Get the delivery schedule
        try:
            schedule = DeliverySchedule.objects.get(schedule_id=schedule_id)
            print(f"Found delivery schedule: {schedule.schedule_id}")
            print(f"Associated invoice number: {schedule.delivery_request.invoice_number}")
        except DeliverySchedule.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': f'Delivery schedule not found: {schedule_id}'
            }, status=404)
        
        # Validate the new status
        valid_statuses = ['Scheduled', 'In-Transit', 'Delivered', 'Cancelled']
        if new_status not in valid_statuses:
            return JsonResponse({
                'status': 'error',
                'message': f'Invalid status: {new_status}'
            }, status=400)
        
        # Use transaction to ensure all updates happen together
        with transaction.atomic():
            # Update the delivery schedule status
            schedule.status = new_status
            schedule.save()
            print(f"Updated delivery schedule status to: {new_status}")
    
            # If status is Delivered, update both delivery request and related order
            if new_status == 'Delivered':
                # Update delivery request status
                schedule.delivery_request.status = 'Completed'
                schedule.delivery_request.save()
                print(f"Updated delivery request status to: Completed")

                # Create notification for aftersales department only for sales orders
                if not schedule.delivery_request.invoice_number.startswith('INVWH-'):
                    create_notification(
                        title='New Delivery Completed',
                        message=f'Delivery {schedule.schedule_id} has been completed for {schedule.delivery_request.client_info.get("client_name")}',
                        notification_type='delivery_complete',
                        from_dept='delivery',
                        to_dept='aftersales',
                        related_id=schedule.id,
                        related_link=f'/aftersales/logs/?schedule_id={schedule.schedule_id}'
                    )

                    # Create notification for sales department only for sales orders
                    create_notification(
                        title='Order Delivered',
                        message=f'Order {schedule.delivery_request.invoice_number} has been delivered to {schedule.delivery_request.client_info.get("client_name")}',
                        notification_type='order_delivered',
                        from_dept='delivery',
                        to_dept='sales',
                        related_id=schedule.id,
                        related_link=f'/sales/orders/?order_number={schedule.delivery_request.invoice_number}'
                    )

                    # Create notification for admin panel for sales delivery
                    create_notification(
                        title='Sales Delivery Completed',
                        message=f'Sales delivery {schedule.schedule_id} has been completed for {schedule.delivery_request.client_info.get("client_name")}',
                        notification_type='sales_delivery_complete',
                        from_dept='delivery',
                        to_dept='admin',
                        related_id=schedule.id,
                        related_link=f'/adminpanel/delivery&Tracking/?schedule_id={schedule.schedule_id}'
                    )

                # Handle warehouse delivery
                if schedule.delivery_request.invoice_number.startswith('INVWH-'):
                    try:
                        # Get warehouse invoice and order
                        warehouse_invoice = WarehouseInvoice.objects.select_related('order').get(
                            invoice_number=schedule.delivery_request.invoice_number
                        )
                        warehouse_order = warehouse_invoice.order

                        # Create or update warehouse client record
                        client_record, created = WarehouseClientRecord.objects.get_or_create(
                            client_name=warehouse_order.client_name,
                            defaults={
                                'company_name': warehouse_order.company_name,
                                'contact_info': warehouse_order.client_contact,
                                'email': warehouse_order.client_email,
                                'address': warehouse_order.client_address,
                                'total_orders': 1,
                                'status': 'Active',
                                'last_order_date': schedule.delivery_date,
                                'delivery_schedule': schedule,
                                'warehouse_order': warehouse_order
                            }
                        )

                        if not created:
                            client_record.total_orders += 1
                            client_record.last_order_date = schedule.delivery_date
                            client_record.delivery_schedule = schedule
                            client_record.warehouse_order = warehouse_order
                            client_record.save()

                        # Update warehouse order status
                        warehouse_order.status = 'Completed'
                        warehouse_order.save()

                        # Create notification for warehouse department
                        create_notification(
                            title='Order Delivered',
                            message=f'Order {warehouse_invoice.invoice_number} has been delivered to {warehouse_order.client_name}',
                            notification_type='warehouse_order_delivered',
                            from_dept='delivery',
                            to_dept='warehouse',
                            related_id=warehouse_order.id,
                            related_link=f'/warehouse/orders/?order_number={warehouse_order.order_number}'
                        )
                        # Create notification for admin panel
                        create_notification(
                            title='Warehouse Delivery Completed',
                            message=f'Warehouse delivery {schedule.schedule_id} has been completed for {warehouse_order.client_name}',
                            notification_type='warehouse_delivery_complete',
                            from_dept='delivery',
                            to_dept='admin',
                            related_id=schedule.id,
                            related_link=f'/adminpanel/delivery&Tracking/?schedule_id={schedule.schedule_id}'
                        )

                        # Reduce inventory
                        unit_info = schedule.delivery_request.unit_info or {}
                        item_code = unit_info.get('item_code')
                        quantity_delivered = int(unit_info.get('quantity', 0))
                        if item_code and quantity_delivered > 0:
                            try:
                                inventory_item = InventoryItem.objects.get(item_code=item_code)
                                if inventory_item.quantity >= quantity_delivered:
                                    inventory_item.quantity -= quantity_delivered
                                    inventory_item.save()
                                    print(f"Reduced inventory for {item_code} by {quantity_delivered}. New quantity: {inventory_item.quantity}")
                                else:
                                    print(f"WARNING: Not enough stock for {item_code}")
                            except InventoryItem.DoesNotExist:
                                print(f"Inventory item not found for code: {item_code}")

                    except WarehouseInvoice.DoesNotExist:
                        print(f"Warehouse invoice not found for number: {schedule.delivery_request.invoice_number}")
                    except Exception as e:
                        print(f"Error processing warehouse delivery: {str(e)}")
                        raise

                # Handle sales delivery
                else:
                    try:
                        # Get the related invoice and sales order
                        invoice = Invoice.objects.select_related('order').get(
                            invoice_number=schedule.delivery_request.invoice_number
                        )
                        print(f"Found invoice: {invoice.invoice_number}")
                        
                        if invoice.order:
                            # Update the sales order status to Completed
                            sales_order = invoice.order
                            print(f"Found sales order: {sales_order.order_number}")
                            print(f"Current sales order status: {sales_order.status}")
                            
                            # Update inventory quantities for each item in the order
                            order_items = sales_order.items.select_related('inventory_item').all()
                            for order_item in order_items:
                                inventory_item = order_item.inventory_item
                                print(f"Updating inventory for item: {inventory_item.item_code}")
                                print(f"Current quantity: {inventory_item.quantity}")
                                print(f"Reducing by: {order_item.quantity}")
                                
                                # Reduce inventory quantity
                                if inventory_item.quantity >= order_item.quantity:
                                    inventory_item.quantity -= order_item.quantity
                                    inventory_item.save()
                                    print(f"New quantity: {inventory_item.quantity}")
                                else:
                                    print(f"WARNING: Not enough inventory for {inventory_item.item_code}")
                            
                            sales_order.status = 'Completed'
                            sales_order.save()
                            
                            # Verify the update
                            refreshed_order = SalesOrder.objects.get(id=sales_order.id)
                            print(f"Updated sales order {sales_order.order_number} status to: {refreshed_order.status}")
                            
                            if refreshed_order.status != 'Completed':
                                print("WARNING: Sales order status not updated correctly!")
                        else:
                            print("No order found for invoice!")
                        
                    except Invoice.DoesNotExist:
                        print(f"Invoice not found for number: {schedule.delivery_request.invoice_number}")
                    except Exception as e:
                        print(f"Error updating sales order status: {str(e)}")
                        print(f"Error type: {type(e)}")
                        import traceback
                        print(f"Traceback: {traceback.format_exc()}")
                        raise  # Re-raise the exception to rollback the transaction
        
        print("=== Delivery status update completed successfully ===\n")
        return JsonResponse({
            'status': 'success',
            'message': 'Delivery status updated successfully'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({
            'status': 'error',
            'message': f'Unexpected error: {str(e)}'
        }, status=500)


