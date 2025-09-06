from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from adminpanel.models import InventoryItem
from adminpanel.forms import InventoryItemForm
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import SalesOrder, OrderItem, Invoice, Request, RequestNote, ClientRecord
from .forms import SalesOrderForm, OrderItemForm
import json
from django.views.decorators.http import require_POST, require_http_methods
from datetime import timedelta
from decimal import Decimal
from django.db.models import Sum
from notifications.views import create_notification


# Create your views here.

def is_sales(user):
    return user.groups.filter(name='Sales').exists()

@login_required
@user_passes_test(is_sales)
def sales_base(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'sales/sales_base.html', {'profile': profile})





@login_required
@user_passes_test(is_sales)
def sales_dashboard(request):
    # Get all completed sales orders
    orders = SalesOrder.objects.filter(status='Completed')
    # Sum the quantity of all items in these orders
    total_units_sold = OrderItem.objects.filter(order__in=orders).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    # Get count of pending orders
    pending_orders_count = SalesOrder.objects.filter(
        status='Pending'
    ).count()

    # Get count of scheduled PDI inspections
    scheduled_pdi_count = Request.objects.filter(
        request_type='PDI'
    ).count()

    return render(request, 'pages/sales_dashboard.html', {
        'total_units_sold': total_units_sold,
        'pending_orders_count': pending_orders_count,
        'scheduled_pdi_count': scheduled_pdi_count,
    })


@login_required
@user_passes_test(is_sales)
def sales_inventory(request):
    # Handle form submission
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, request.FILES)  # Handle file uploads for `photo`
        if form.is_valid():
            new_item = form.save()  # Save the new inventory item
            # Send notification to admin panel
            title = "New Inventory Added (Sales)"
            message = f"A new inventory item ('{new_item.unit_item}') was added by Sales."
            notification_type = "inventory_added"
            from_dept = "sales"
            to_dept = "admin"
            # Link to adminpanel inventory page
            related_link = "/adminpanel/inventory/"
            create_notification(title, message, notification_type, from_dept, to_dept, related_id=new_item.id, related_link=related_link)
            return redirect('sales_inventory')  # Redirect to the same page after saving
    else:
        form = InventoryItemForm()  # Display an empty form for GET requests

    # Fetch all inventory items
    items = InventoryItem.objects.filter(department='Sales')

    # Calculate dashboard metrics
    total_quantity = items.aggregate(total=Sum('quantity'))['total'] or 0
    low_stock_items = items.filter(quantity__lt=20).count()
    
    # Get items added this week using date_received
    one_week_ago = timezone.now().date() - timedelta(days=7)
    new_items_this_week = items.filter(date_received__gte=one_week_ago).count()

    return render(request, 'pages/sales_inventory.html', {
        'items': items, 
        'form': form,
        'total_items': total_quantity,  # Now represents total quantity
        'low_stock_items': low_stock_items,
        'new_items_this_week': new_items_this_week
    })



@login_required
@user_passes_test(is_sales)
def sales_forecasting(request):
    return render(request, 'pages/sales_forecasting.html')



@login_required
@user_passes_test(is_sales)
def sales_equipment(request):
    items = InventoryItem.objects.filter(department='Sales')  # Assuming you have a department field in your InventoryItem model

    return render(request, 'pages/sales_equipment.html', {'items': items})



@login_required
@user_passes_test(is_sales)
def sales_orders(request):
    # Get all orders with a fresh query, ordered by most recent first
    orders = SalesOrder.objects.all().order_by('-created_at').select_related()
    
    # Force evaluation of the queryset to ensure fresh data
    orders = list(orders)
    
    # Add inventory items for the dropdown in the request orders modal
    items = InventoryItem.objects.filter(department='Sales')
    
    # Add today's date for the order date field
    today = timezone.now().date()
    
    return render(request, 'pages/sales_orders.html', {
        'orders': orders,
        'items': items,
        'today': today
    })



@login_required
@user_passes_test(is_sales)
def sales_invoicing(request):
    # Update invoice statuses before displaying
    update_invoice_statuses()
    
    # Get all invoices ordered by creation date with PDI request info
    invoices = Invoice.objects.all().order_by('-created_at')
    
    # Add PDI request info to each invoice
    for invoice in invoices:
        invoice.has_pdi_request = Request.objects.filter(
            invoice_number=invoice.invoice_number,
            request_type='PDI'
        ).exists()
    
    return render(request, 'pages/sales_invoicing.html', {'invoices': invoices})



@login_required
@user_passes_test(is_sales)
def sales_client_records(request):
    client_records = ClientRecord.objects.all()
    # Attach the latest SalesOrder for each client
    for client in client_records:
        latest_order = SalesOrder.objects.filter(client_name=client.client_name).order_by('-order_date').first()
        client.latest_order = latest_order
    return render(request, 'pages/sales_client_records.html', {
        'client_records': client_records
    })


@login_required
@user_passes_test(is_sales)
def sales_received_requests(request):
    return render(request, 'pages/internal_requests/sales_received_requests.html')



@login_required
@user_passes_test(is_sales)
def sales_sent_requests(request):
    # Get requests with related invoice data
    requests = Request.objects.filter(requested_by=request.user).order_by('-created_at')
    
    # Create a dictionary to store invoice data for each request
    request_data = []
    for req in requests:
        try:
            invoice = Invoice.objects.get(invoice_number=req.invoice_number)
            request_data.append({
                'request': req,
                'invoice': invoice
            })
        except Invoice.DoesNotExist:
            request_data.append({
                'request': req,
                'invoice': None
            })
    
    return render(request, 'pages/internal_requests/sales_sent_requests.html', {
        'request_data': request_data
    })


@login_required
@user_passes_test(is_sales)
def sales_restock_inventory(request, item_id):
    item = get_object_or_404(InventoryItem, id=item_id, department='Sales')
    
    if request.method == 'POST':
        try:
            quantity_to_add = int(request.POST.get('quantity_to_add'))
            supplier = request.POST.get('supplier')
            date_received = request.POST.get('date_received')
            new_unit_price = request.POST.get('new_unit_price')
            
            if quantity_to_add <= 0:
                messages.error(request, 'Quantity to add must be greater than 0')
                return redirect('sales_inventory')
            
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
                    return redirect('sales_inventory')
                    
            item.save()
            
            messages.success(request, f'Successfully restocked {item.unit_item} with {quantity_to_add} units')
        except ValueError:
            messages.error(request, 'Invalid quantity value')
        except Exception as e:
            messages.error(request, f'Error restocking item: {str(e)}')
    
    return redirect('sales_inventory')





@login_required
@user_passes_test(is_sales)
def sales_settings(request):
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
            return redirect('sales_settings')
    
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
    
    return render(request, 'pages/sales_settings.html', context)

@login_required
@user_passes_test(is_sales)
def create_sales_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.POST.get('order_data', '{}'))
            
            # Create SalesOrder
            order = SalesOrder.objects.create(
                client_name=data.get('client_name'),
                client_address=data.get('client_address'),
                client_contact=data.get('client_contact'),
                client_email=data.get('client_email'),
                company_name=data.get('company_name'),
                company_address=data.get('company_address'),
                company_contact=data.get('company_contact'),
                company_email=data.get('company_email'),
                delivery_date=data.get('delivery_date'),
                delivery_instructions=data.get('delivery_instructions'),
                payment_mode=data.get('payment_mode'),
                due_date=data.get('due_date'),
                amount_paid=data.get('amount_paid', 0),
                residence_location=data.get('residence_location'),
                bank_account=data.get('bank_account'),
                account_number=data.get('account_number')
            )
            
            # Handle file uploads
            if request.FILES.get('id_attachment'):
                order.id_attachment = request.FILES['id_attachment']
            if request.FILES.get('business_permit'):
                order.business_permit = request.FILES['business_permit']
            if request.FILES.get('bir_attachment'):
                order.bir_attachment = request.FILES['bir_attachment']
            
            # Calculate total amount
            total_amount = 0
            for item_data in data.get('items', []):
                inventory_item = InventoryItem.objects.get(id=item_data['item_id'])
                quantity = int(item_data['quantity'])
                unit_price = float(item_data['unit_price'])
                total_amount += quantity * unit_price
                
                OrderItem.objects.create(
                    order=order,
                    inventory_item=inventory_item,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=quantity * unit_price
                )
            
            order.total_amount = total_amount
            order.save()

            # Create Invoice automatically
            # Determine invoice status based on payment
            invoice_status = 'Paid' if float(order.amount_paid) >= float(total_amount) else 'Pending'
            
            invoice = Invoice.objects.create(
                order=order,
                client_name=order.client_name,
                amount=order.total_amount,
                invoice_date=timezone.now().date(),
                due_date=order.due_date,
                status=invoice_status  # Set the status based on payment
            )

            # Create notification for admin panel about new invoice
            create_notification(
                title='New Invoice Generated',
                message=f'New invoice {invoice.invoice_number} has been generated for {order.client_name}',
                notification_type='new_invoice',
                from_dept='sales',
                to_dept='admin',
                related_id=invoice.id,
                related_link=f'/adminpanel/invoicing/?invoice_number={invoice.invoice_number}'
            )

            # Create notification for admin panel about new order
            create_notification(
                title='New Sales Order Created',
                message=f'New order {order.order_number} has been created for {order.client_name}',
                notification_type='new_sales_order',
                from_dept='sales',
                to_dept='admin',
                related_id=order.id,
                related_link=f'/adminpanel/sales&Orders/?order_number={order.order_number}'
            )

            return JsonResponse({'status': 'success', 'message': 'Order created successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
@user_passes_test(is_sales)
def get_item_details(request, item_id):
    try:
        item = InventoryItem.objects.get(id=item_id)
        return JsonResponse({
            'item_code': item.item_code,
            'serial_number': item.serial_number,
            'unit_price': str(item.unit_price) if item.unit_price else '0.00',  # Use actual unit price from item
            'available_quantity': item.quantity
        })
    except InventoryItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)

@login_required
@user_passes_test(is_sales)
def update_sales_order(request, order_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.POST.get('order_data', '{}'))
            order = get_object_or_404(SalesOrder, id=order_id)
            
            # Update SalesOrder
            order.client_name = data.get('client_name')
            order.client_address = data.get('client_address')
            order.client_contact = data.get('client_contact')
            order.client_email = data.get('client_email')
            order.company_name = data.get('company_name')
            order.company_address = data.get('company_address')
            order.company_contact = data.get('company_contact')
            order.company_email = data.get('company_email')
            order.delivery_date = data.get('delivery_date')
            order.delivery_instructions = data.get('delivery_instructions')
            order.payment_mode = data.get('payment_mode')
            order.due_date = data.get('due_date')
            order.amount_paid = data.get('amount_paid', 0)
            order.residence_location = data.get('residence_location')
            order.bank_account = data.get('bank_account')
            order.account_number = data.get('account_number')
            
            # Handle file uploads if new files are provided
            if request.FILES.get('id_attachment'):
                order.id_attachment = request.FILES['id_attachment']
            if request.FILES.get('business_permit'):
                order.business_permit = request.FILES['business_permit']
            if request.FILES.get('bir_attachment'):
                order.bir_attachment = request.FILES['bir_attachment']
            
            # Update or create OrderItems
            items_data = data.get('items', [])
            total_amount = 0
            
            # Remove existing items
            order.items.all().delete()
            
            # Create new items
            for item_data in items_data:
                inventory_item = InventoryItem.objects.get(id=item_data['item_id'])
                quantity = int(item_data['quantity'])
                unit_price = float(item_data['unit_price'])
                
                OrderItem.objects.create(
                    order=order,
                    inventory_item=inventory_item,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=quantity * unit_price
                )
                
                total_amount += quantity * unit_price
            
            # Update the total amount
            order.total_amount = total_amount
            order.save()

            # Update invoice status if it exists
            try:
                invoice = Invoice.objects.get(order=order)
                invoice.amount = total_amount
                invoice.due_date = order.due_date
                # Update status based on payment
                if float(order.amount_paid) >= float(total_amount):
                    invoice.status = 'Paid'
                elif invoice.status != 'Overdue':  # Don't change if it's overdue
                    invoice.status = 'Pending'
                invoice.save()
            except Invoice.DoesNotExist:
                pass

            return JsonResponse({'status': 'success', 'message': 'Order updated successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
@user_passes_test(is_sales)
def get_order_details(request, order_id):
    try:
        order = SalesOrder.objects.get(id=order_id)
        items = []
        for item in order.items.all():
            items.append({
                'item_id': item.inventory_item.id,
                'item_name': item.inventory_item.unit_item,
                'item_code': item.inventory_item.item_code,
                'serial_number': item.inventory_item.serial_number,
                'quantity': item.quantity,
                'unit_price': str(item.unit_price),
                'total_price': str(item.total_price)
            })
            
        data = {
            'order_number': order.order_number,
            'client_name': order.client_name,
            'client_address': order.client_address,
            'client_contact': order.client_contact,
            'client_email': order.client_email,
            'company_name': order.company_name,
            'company_address': order.company_address,
            'company_contact': order.company_contact,
            'company_email': order.company_email,
            'delivery_date': order.delivery_date.strftime('%Y-%m-%d'),
            'delivery_instructions': order.delivery_instructions,
            'payment_mode': order.payment_mode,
            'due_date': order.due_date.strftime('%Y-%m-%d'),
            'amount_paid': str(order.amount_paid),
            'residence_location': order.residence_location,
            'bank_account': order.bank_account,
            'account_number': order.account_number,
            'total_amount': str(order.total_amount),
            'items': items
        }
        return JsonResponse(data)
    except SalesOrder.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)

@require_POST
def cancel_order(request, order_id):
    try:
        order = SalesOrder.objects.get(id=order_id)
        order.status = 'Cancelled'
        order.save()
        
        # Update the corresponding invoice status
        try:
            invoice = Invoice.objects.get(order=order)
            invoice.status = 'Cancelled'
            invoice.save()
        except Invoice.DoesNotExist:
            pass  # No invoice exists for this order
            
        return JsonResponse({'status': 'success'})
    except SalesOrder.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Order not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def update_invoice_statuses():
    today = timezone.now().date()
    # Update overdue invoices - only update if not already Paid or Cancelled
    Invoice.objects.filter(
        due_date__lt=today,  # due_date is less than today
        status='Pending'     # only update Pending invoices
    ).update(status='Overdue')

@login_required
@user_passes_test(is_sales)
@require_POST
def update_payment(request):
    try:
        invoice_id = request.POST.get('invoice_id')
        amount = request.POST.get('amount')
        new_due_date = request.POST.get('new_due_date')

        invoice = Invoice.objects.get(id=invoice_id)
        order = invoice.order

        # Convert amount to Decimal for proper decimal arithmetic
        amount = Decimal(amount)

        # Validate payment amount
        if amount <= 0:
            return JsonResponse({'status': 'error', 'message': 'Payment amount must be greater than 0'})
        if amount > order.remaining_balance:
            return JsonResponse({'status': 'error', 'message': 'Payment amount cannot exceed remaining balance'})

        # Update order's amount paid
        order.amount_paid += amount
        order.save()

        # Update invoice status and due date
        if order.remaining_balance == 0:
            invoice.status = 'Paid'
        
        # Update due date if provided
        if new_due_date:
            from datetime import datetime
            invoice.due_date = datetime.strptime(new_due_date, '%Y-%m-%d').date()
            # Reset status to Pending if it was Overdue and new due date is set
            if invoice.status == 'Overdue':
                invoice.status = 'Pending'
        
        invoice.save()

        return JsonResponse({'status': 'success'})
    except Invoice.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invoice not found'})
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Invalid amount'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
@user_passes_test(is_sales)
@require_POST
def check_overdue(request):
    try:
        # Get current server time
        current_time = timezone.now().date()
        
        # Find and update overdue invoices
        updated = Invoice.objects.filter(
            due_date__lt=current_time,
            status='Pending'
        ).update(status='Overdue')
        
        return JsonResponse({'status': 'success', 'updated': updated > 0})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_http_methods(["POST"])
def create_pdi_request(request):
    try:
        data = json.loads(request.body)
        
        # Generate request ID: RQ-YYYYMMDD-XXXX
        date_str = timezone.now().strftime('%Y%m%d')
        last_request = Request.objects.filter(request_id__startswith=f'RQ-{date_str}').order_by('request_id').last()
        
        if last_request:
            last_number = int(last_request.request_id.split('-')[-1])
            new_number = str(last_number + 1).zfill(4)
        else:
            new_number = '0001'
        
        request_id = f'RQ-{date_str}-{new_number}'
        
        # Get user's full name
        requested_by_name = f"{request.user.first_name} {request.user.last_name}"
        if not requested_by_name.strip():  # If first_name and last_name are empty
            requested_by_name = request.user.username
        
        # Create new request
        new_request = Request.objects.create(
            request_id=request_id,
            request_type='PDI',
            unit=data['unit'],
            invoice_number=data['invoice_number'],
            invoice_id=data['invoice_id'],
            requested_by=request.user,
            requested_by_name=requested_by_name,  # Add the full name
            assigned_to='Motorpool',
            status='Pending'
        )
        
        # Create notification for motorpool department
        create_notification(
            title='New PDI Request',
            message=f'New PDI request ({request_id}) for unit {data["unit"]} from {requested_by_name}',
            notification_type='pdi_request',
            from_dept='sales',
            to_dept='motorpool',
            related_id=new_request.id,
            related_link=f'/motorpool/received_requests/?request_id={request_id}'
        )

        # Create notification for admin panel
        create_notification(
            title='New PDI Request',
            message=f'New PDI request ({request_id}) for unit {data["unit"]} from {requested_by_name}',
            notification_type='pdi_request_admin',
            from_dept='sales',
            to_dept='admin',
            related_id=new_request.id,
            related_link=f'/adminpanel/motorpool/?request_id={request_id}'
        )

        return JsonResponse({
            'status': 'success',
            'message': 'PDI request created successfully',
            'request_id': request_id
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@user_passes_test(is_sales)
@require_http_methods(["POST"])
def update_request_notes(request):
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
        req = Request.objects.get(id=request_id, requested_by=request.user)
        
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

def client_orders(request, client_id):
    client = get_object_or_404(ClientRecord, id=client_id)
    orders = SalesOrder.objects.filter(client_record=client).order_by('-order_date')
    orders_data = [{
        'id': order.id,
        'order_number': order.order_number,
        'item_description': order.item_description,
        'total_amount': order.total_amount,
        'order_date': order.order_date,
        'delivery_date': order.delivery_date,
        'status': order.status
    } for order in orders]
    return JsonResponse({'orders': orders_data})

def client_invoices(request, client_id):
    client = get_object_or_404(ClientRecord, id=client_id)
    invoices = Invoice.objects.filter(client_record=client).order_by('-invoice_date')
    invoices_data = [{
        'id': invoice.id,
        'invoice_number': invoice.invoice_number,
        'amount': invoice.amount,
        'invoice_date': invoice.invoice_date,
        'due_date': invoice.due_date,
        'status': invoice.status
    } for invoice in invoices]
    return JsonResponse({'invoices': invoices_data})

@login_required
@user_passes_test(is_sales)
def request_pdi(request, invoice_id):
    try:
        invoice = Invoice.objects.get(id=invoice_id)
        
        # Create PDI request
        pdi_request = PDIRequest.objects.create(
            invoice=invoice,
            status='Pending'
        )
        
        # Create notification for motorpool department
        create_notification(
            title='New PDI Request',
            message=f'New PDI request for invoice #{invoice.invoice_number}',
            notification_type='pdi_request',
            from_dept='sales',
            to_dept='motorpool',
            related_id=pdi_request.id,
            related_link=f'/motorpool/received_requests/?request_id={pdi_request.id}'
        )
        
        return JsonResponse({'status': 'success', 'message': 'PDI request created successfully'})
    except Invoice.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invoice not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)



