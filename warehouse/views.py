from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from adminpanel.models import InventoryItem
from adminpanel.forms import InventoryItemForm
from django.contrib import messages
from django.utils import timezone
from adminpanel.models import UserProfile
from .models import WarehouseOrder, WarehouseOrderItem, WarehouseInvoice, WarehouseClientRecord
from django.http import JsonResponse
import json
from decimal import Decimal
from django.views.decorators.http import require_http_methods, require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from delivery.models import DeliveryRequest
from django.db.models import Sum
from datetime import timedelta
from notifications.views import create_notification
# Create your views here.

def is_warehouse(user):
    return user.groups.filter(name='Warehouse').exists()

@login_required
@user_passes_test(is_warehouse)
def warehouse_base(request):
    # Get the current user's profile
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'warehouse/warehouse_base.html', {'profile': profile})



@login_required
@user_passes_test(is_warehouse)
def warehouse_dashboard(request):
    # Get total spare parts in stock
    total_spare_parts = InventoryItem.objects.filter(department='Warehouse').aggregate(
        total=Sum('quantity')
    )['total'] or 0

    # Get count of pending orders
    pending_orders = WarehouseOrder.objects.filter(status='Pending').count()

    # Get count of completed orders this month
    current_month = timezone.now().month
    current_year = timezone.now().year
    parts_delivered = WarehouseOrder.objects.filter(
        status='Completed',
        order_date__month=current_month,
        order_date__year=current_year
    ).count()

    return render(request, 'pages/warehouse_dashboard.html', {
        'total_spare_parts': total_spare_parts,
        'pending_orders': pending_orders,
        'parts_delivered': parts_delivered
    })


@login_required
@user_passes_test(is_warehouse)
def warehouse_inventory(request):
    # Handle form submission
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, request.FILES)  # Handle file uploads for `photo`
        if form.is_valid():
            new_item = form.save()  # Save the new inventory item
            # Send notification to admin panel
            title = "New Inventory Added"
            message = f"A new inventory item ('{new_item.unit_item}') was added by Warehouse."
            notification_type = "inventory_added"
            from_dept = "warehouse"
            to_dept = "admin"
            # Link to adminpanel inventory page
            related_link = "/adminpanel/inventory/"
            create_notification(title, message, notification_type, from_dept, to_dept, related_id=new_item.id, related_link=related_link)
            return redirect('warehouse_inventory')  # Redirect to the same page after saving
    else:
        form = InventoryItemForm()  # Display an empty form for GET requests

    # Fetch all inventory items     
    items = InventoryItem.objects.filter(department='Warehouse')

    # Calculate dashboard metrics
    total_items = items.aggregate(total=Sum('quantity'))['total'] or 0
    low_stock_items = items.filter(quantity__lt=20).count()
    
    # Get items added this week using date_received
    one_week_ago = timezone.now().date() - timedelta(days=7)
    new_items_this_week = items.filter(date_received__gte=one_week_ago).count()

    return render(request, 'pages/inventory.html', {
        'items': items, 
        'form': form,
        'total_items': total_items,
        'low_stock_items': low_stock_items,
        'new_items_this_week': new_items_this_week
    })




@login_required
@user_passes_test(is_warehouse)
def warehouse_forecast(request):
    return render(request, 'pages/forecast.html')


@login_required
@user_passes_test(is_warehouse)
def warehouse_spare_parts_listing(request):
    items = InventoryItem.objects.filter(department='Warehouse')  # Assuming you have a department field in your InventoryItem model

    return render(request, 'pages/spare_parts_listing.html', {'items': items})



@login_required
@user_passes_test(is_warehouse)
def warehouse_orders(request):
    orders = WarehouseOrder.objects.all().order_by('-order_date')
    inventory_items = InventoryItem.objects.filter(department='Warehouse')
    return render(request, 'pages/orders.html', {
        'orders': orders,
        'items': inventory_items,  # For modal dropdown compatibility
        'inventory_items': inventory_items,
        'today': timezone.now()
    })



@login_required
@user_passes_test(is_warehouse)
def warehouse_client_records(request):
    clients = WarehouseClientRecord.objects.all()
    return render(request, 'pages/client_records.html', {'clients': clients})



@login_required
@user_passes_test(is_warehouse)
def warehouse_received_requests(request):
    return render(request, 'pages/internal_requests/warehouse_received_requests.html')




@login_required
@user_passes_test(is_warehouse)
def warehouse_sent_requests(request):
    return render(request, 'pages/internal_requests/warehouse_sent_requests.html')


@login_required
@user_passes_test(is_warehouse)
def restock_inventory(request, item_id):
    item = get_object_or_404(InventoryItem, id=item_id)
    
    if request.method == 'POST':
        try:
            quantity_to_add = int(request.POST.get('quantity_to_add'))
            supplier = request.POST.get('supplier')
            date_received = request.POST.get('date_received')
            new_unit_price = request.POST.get('new_unit_price')
            
            if quantity_to_add <= 0:
                messages.error(request, 'Quantity to add must be greater than 0')
                return redirect('warehouse_inventory')
            
            # Update the item
            item.quantity += quantity_to_add
            item.supplier = supplier
            item.date_received = date_received
            
            # Update unit price if provided
            if new_unit_price:
                try:
                    item.unit_price = float(new_unit_price)
                except ValueError:
                    messages.error(request, 'Invalid unit price value')
                    return redirect('warehouse_inventory')
                    
            item.save()
            # Send notification to admin panel
            title = "Inventory Restocked"
            message = f"{quantity_to_add} units were added to '{item.unit_item}' by Warehouse."
            notification_type = "inventory_restocked"
            from_dept = "warehouse"
            to_dept = "admin"
            related_link = "/adminpanel/inventory/"
            create_notification(title, message, notification_type, from_dept, to_dept, related_id=item.id, related_link=related_link)
            messages.success(request, f'Successfully restocked {item.unit_item} with {quantity_to_add} units')
        except ValueError:
            messages.error(request, 'Invalid quantity value')
        except Exception as e:
            messages.error(request, f'Error restocking item: {str(e)}')
    
    return redirect('warehouse_inventory')




@login_required
@user_passes_test(is_warehouse)
def warehouse_settings(request):
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
            timezone_value = request.POST.get('timezone')
            date_format = request.POST.get('dateFormat')

            if timezone_value:
                user_settings.timezone = timezone_value
            if date_format:
                user_settings.date_format = date_format

            user_settings.save()
            messages.success(request, 'Settings saved successfully!')
            return redirect('warehouse_settings')

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

    return render(request, 'pages/warehouse_settings.html', context)



@login_required
@user_passes_test(is_warehouse)
def warehouse_invoice(request):
    invoices = WarehouseInvoice.objects.select_related('order').all().order_by('-invoice_date')
    from delivery.models import DeliveryRequest
    for invoice in invoices:
        invoice.has_delivery_request = DeliveryRequest.objects.filter(invoice_number=invoice.invoice_number).exists()
    return render(request, 'pages/warehouse_invoice.html', {'invoices': invoices})

@login_required
@require_http_methods(["POST"])
def create_order(request):
    try:
        data = request.POST
        files = request.FILES

        # Parse order_data JSON
        order_data = json.loads(data.get('order_data'))

        # Create the order
        order = WarehouseOrder.objects.create(
            client_name=order_data.get('client_name'),
            client_contact=order_data.get('client_contact'),
            client_email=order_data.get('client_email'),
            client_address=order_data.get('client_address'),
            company_name=order_data.get('company_name'),
            company_address=order_data.get('company_address'),
            company_contact=order_data.get('company_contact'),
            company_email=order_data.get('company_email'),
            order_date=timezone.now(),
            delivery_date=order_data.get('delivery_date'),
            delivery_instructions=order_data.get('delivery_instructions'),
            payment_mode=order_data.get('payment_mode'),
            due_date=order_data.get('due_date') if order_data.get('due_date') else None,
            amount_paid=Decimal(order_data.get('amount_paid', 0)),
            residence_location=order_data.get('residence_location'),
            bank_account=order_data.get('bank_account'),
            account_number=order_data.get('account_number'),
            created_by=request.user
        )

        # Handle file attachments
        if 'id_attachment' in files:
            order.id_attachment = files['id_attachment']
        if 'permit_attachment' in files:
            order.permit_attachment = files['permit_attachment']
        if 'business_permit' in files:
            order.business_permit = files['business_permit']
        if 'bir_attachment' in files:
            order.bir_attachment = files['bir_attachment']
        order.save()

        # Create order items
        items = order_data.get('items', [])
        for item in items:
            if item.get('item_id') and item.get('quantity'):
                inventory_item = InventoryItem.objects.get(id=item['item_id'])
                WarehouseOrderItem.objects.create(
                    order=order,
                    inventory_item=inventory_item,
                    quantity=int(item['quantity']),
                    unit_price=Decimal(item['unit_price']),
                    item_code=item.get('item_code', ''),
                    serial_number=item.get('serial_number', '')
                )

        # Update total_amount for the order
        order.total_amount = sum(item.quantity * item.unit_price for item in order.items.all())
        order.save()

        # Automatically create invoice for the order
        date_str = timezone.now().strftime('%Y%m%d')
        last_invoice = WarehouseInvoice.objects.filter(invoice_number__startswith=f'INVWH-{date_str}').order_by('invoice_number').last()
        if last_invoice:
            last_number = int(last_invoice.invoice_number.split('-')[-1])
            new_number = str(last_number + 1).zfill(4)
        else:
            new_number = '0001'
        invoice_number = f'INVWH-{date_str}-{new_number}'
        
        # Determine invoice status based on payment
        invoice_status = 'Paid' if order.amount_paid >= order.total_amount else 'Pending'
        
        WarehouseInvoice.objects.create(
            order=order,
            invoice_number=invoice_number,
            status=invoice_status,  # Set status based on payment
            invoice_date=timezone.now(),
            due_date=order.due_date,
            amount=order.total_amount
        )

        # Create notification for admin panel (order)
        create_notification(
            title='New Warehouse Order Created',
            message=f'New warehouse order {order.order_number} has been created for {order.client_name}',
            notification_type='new_warehouse_order',
            from_dept='warehouse',
            to_dept='admin',
            related_id=order.id,
            related_link=f'/adminpanel/sales&Orders/?order_number={order.order_number}'
        )

        # Create notification for admin panel (invoice)
        create_notification(
            title='New Warehouse Invoice Generated',
            message=f'New invoice {invoice_number} has been generated for {order.client_name}',
            notification_type='new_warehouse_invoice',
            from_dept='warehouse',
            to_dept='admin',
            related_id=None,
            related_link=f'/adminpanel/invoicing/?invoice_number={invoice_number}'
        )

        return JsonResponse({
            'status': 'success',
            'message': 'Order created successfully',
            'order_id': order.id
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
def get_item_details(request, item_id):
    try:
        item = InventoryItem.objects.get(id=item_id)
        return JsonResponse({
            'unit_price': str(item.unit_price),
            'unit_item': item.unit_item,
            'item_code': item.item_code,
            'serial_number': item.serial_number,
        })
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_POST
def update_order(request, order_id):
    try:
        order = WarehouseOrder.objects.get(id=order_id)
        order_data = json.loads(request.POST.get('order_data'))

        # Update order fields
        order.client_name = order_data.get('client_name')
        order.client_address = order_data.get('client_address')
        order.client_contact = order_data.get('client_contact')
        order.client_email = order_data.get('client_email')
        order.company_name = order_data.get('company_name')
        order.company_address = order_data.get('company_address')
        order.company_contact = order_data.get('company_contact')
        order.company_email = order_data.get('company_email')
        order.delivery_date = order_data.get('delivery_date')
        order.delivery_instructions = order_data.get('delivery_instructions')
        order.payment_mode = order_data.get('payment_mode')
        order.due_date = order_data.get('due_date')
        order.amount_paid = order_data.get('amount_paid')
        order.residence_location = order_data.get('residence_location')
        order.bank_account = order_data.get('bank_account')
        order.account_number = order_data.get('account_number')
        order.save()

        # Update items: delete all and recreate
        order.items.all().delete()
        for item in order_data.get('items', []):
            if item.get('item_id') and item.get('quantity'):
                inventory_item = InventoryItem.objects.get(id=item['item_id'])
                WarehouseOrderItem.objects.create(
                    order=order,
                    inventory_item=inventory_item,
                    quantity=int(item['quantity']),
                    unit_price=Decimal(item['unit_price']),
                    item_code=item.get('item_code', ''),
                    serial_number=item.get('serial_number', '')
                )

        # Update total_amount
        order.total_amount = sum(item.quantity * item.unit_price for item in order.items.all())
        order.save()

        return JsonResponse({'status': 'success', 'message': 'Order updated successfully!'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
@require_POST
def update_payment(request):
    try:
        invoice_id = request.POST.get('invoice_id')
        amount = Decimal(request.POST.get('amount', 0))
        new_due_date = request.POST.get('new_due_date')

        invoice = WarehouseInvoice.objects.select_related('order').get(id=invoice_id)
        order = invoice.order

        # Update payment
        order.amount_paid += amount
        if new_due_date:
            invoice.due_date = new_due_date
            order.due_date = new_due_date
        order.save()
        invoice.save()

        # Optionally update invoice status
        if order.amount_paid >= invoice.amount:
            invoice.status = 'Paid'
        elif order.amount_paid > 0:
            invoice.status = 'Partial'
        else:
            invoice.status = 'Pending'
        invoice.save()

        return JsonResponse({'status': 'success', 'message': 'Payment updated successfully!'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
@require_POST
def cancel_order(request, order_id):
    try:
        order = WarehouseOrder.objects.get(id=order_id)
        order.status = 'Cancelled'
        order.save()
        
        # Update the corresponding invoice status
        try:
            invoice = WarehouseInvoice.objects.get(order=order)
            invoice.status = 'Cancelled'
            invoice.save()
        except WarehouseInvoice.DoesNotExist:
            pass  # No invoice exists for this order
            
        return JsonResponse({'status': 'success', 'message': 'Order cancelled successfully!'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
@require_POST
def send_to_delivery(request):
    try:
        data = json.loads(request.body)
        invoice_id = data.get('invoice_id')
        invoice_number = data.get('invoice_number')
        client_info = data.get('client_info', {})
        unit_info = data.get('unit_info', {})
        
        invoice = WarehouseInvoice.objects.select_related('order').get(id=invoice_id)
        order = invoice.order
        first_item = order.items.first()
        if first_item:
            unit_info = {
                'unit_name': first_item.inventory_item.unit_item,
                'serial_number': first_item.inventory_item.serial_number,
                'quantity': first_item.quantity,
                'unit_price': str(first_item.unit_price),
                'total_price': str(first_item.total_price),
                'amount_paid': str(order.amount_paid),
                'outstanding_balance': str(order.remaining_balance),
                'delivery_date': str(order.delivery_date),
                'delivery_instructions': order.delivery_instructions or '',
                'item_code': first_item.inventory_item.item_code,
            }
        
        # Create delivery request
        from delivery.models import DeliveryRequest
        
        # Check if delivery request already exists
        existing_request = DeliveryRequest.objects.filter(invoice_number=invoice.invoice_number).first()
        if existing_request:
            return JsonResponse({
                'status': 'error',
                'message': 'A delivery request already exists for this invoice.'
            }, status=400)
            
        # Create new delivery request
        delivery_request = DeliveryRequest.objects.create(
            pdi_request_id='',  # Empty since this is from warehouse
            invoice_number=invoice.invoice_number,
            unit_info=unit_info,
            client_info=client_info,
            status='Pending'
        )

        # Create notification for delivery department
        create_notification(
            title='New Warehouse Delivery Request',
            message=f'New delivery request for {client_info.get("client_name")} - {first_item.inventory_item.unit_item if first_item else "N/A"}',
            notification_type='warehouse_delivery',
            from_dept='warehouse',
            to_dept='delivery',
            related_id=delivery_request.id,
            related_link=f'/delivery/requests/?request_id={delivery_request.request_id}'
        )
            
        # Update order status to Processing
        order = invoice.order
        order.status = 'Processing'
        order.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Invoice sent to delivery successfully',
            'request_id': delivery_request.request_id
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@user_passes_test(is_warehouse)
def get_client_orders(request, client_id):
    try:
        client = WarehouseClientRecord.objects.get(id=client_id)
        orders = WarehouseOrder.objects.filter(client_name=client.client_name).order_by('-order_date')
        
        orders_data = []
        for order in orders:
            first_item = order.items.first()
            orders_data.append({
                'id': order.id,
                'order_number': order.order_number,
                'item_description': first_item.inventory_item.unit_item if first_item else 'N/A',
                'total_amount': str(order.total_amount),
                'order_date': order.order_date.strftime('%Y-%m-%d'),
                'delivery_date': order.delivery_date.strftime('%Y-%m-%d'),
                'status': order.status,
                'id_attachment': order.id_attachment.url if order.id_attachment else ''
            })
        
        return JsonResponse({'orders': orders_data})
    except WarehouseClientRecord.DoesNotExist:
        return JsonResponse({'error': 'Client not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@user_passes_test(is_warehouse)
def get_client_invoices(request, client_id):
    try:
        client = WarehouseClientRecord.objects.get(id=client_id)
        invoices = WarehouseInvoice.objects.filter(order__client_name=client.client_name).order_by('-invoice_date')
        
        invoices_data = []
        for invoice in invoices:
            invoices_data.append({
                'id': invoice.id,
                'invoice_number': invoice.invoice_number,
                'amount': str(invoice.amount),
                'invoice_date': invoice.invoice_date.strftime('%Y-%m-%d'),
                'due_date': invoice.due_date.strftime('%Y-%m-%d'),
                'status': invoice.status
            })
        
        return JsonResponse({'invoices': invoices_data})
    except WarehouseClientRecord.DoesNotExist:
        return JsonResponse({'error': 'Client not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)





