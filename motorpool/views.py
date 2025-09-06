from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from adminpanel.models import UserProfile
from sales.models import Request, RequestNote, Invoice
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import EquipmentInspection
import json
from datetime import datetime
from django.core.files.base import ContentFile
import base64
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from django.conf import settings
from delivery.models import DeliveryRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from notifications.views import create_notification
from django.contrib import messages

# Create your views here.

def is_motorpool(user):
    return user.groups.filter(name='Motorpool').exists()

@login_required
@user_passes_test(is_motorpool)
def motorpool_base(request):
        # Get the current user's profile
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'motorpool/motorpool_base.html', {'profile': profile})





@login_required
@user_passes_test(is_motorpool)
def motorpool_dashboard(request):
    # Get PDI requests assigned to motorpool
    sales_requests = Request.objects.filter(
        request_type='PDI',
        assigned_to='Motorpool'
    ).order_by('-created_at')

    # Get invoice data for each request
    for req in sales_requests:
        try:
            req.invoice = Invoice.objects.get(invoice_number=req.invoice_number)
        except Invoice.DoesNotExist:
            req.invoice = None

    # Calculate metrics for dashboard cards
    pending_pdi_requests = sales_requests.filter(status='Pending').count()
    repairs_in_progress = sales_requests.filter(status='In Progress').count()
    
    # Get completed requests (matching the received requests table)
    completed_inspections = sales_requests.filter(status='Completed').count()

    return render(request, 'pages/motorpool_dashboard.html', {
        'sales_requests': sales_requests,
        'pending_pdi_requests': pending_pdi_requests,
        'repairs_in_progress': repairs_in_progress,
        'completed_inspections': completed_inspections,
    })



@login_required
@user_passes_test(is_motorpool)
def motorpool_received_requests(request):
    # Get PDI requests assigned to motorpool
    sales_requests = Request.objects.filter(
        request_type='PDI',
        assigned_to='Motorpool'
    ).order_by('-created_at')
    
    # Get invoice data for each request
    for req in sales_requests:
        try:
            req.invoice = Invoice.objects.get(invoice_number=req.invoice_number)
        except Invoice.DoesNotExist:
            req.invoice = None
            
        # Check if there's an equipment inspection with Delivery status
        try:
            inspection = EquipmentInspection.objects.get(pdi_request=req)
            if inspection.status == 'Delivery':
                # Update request status to Completed if inspection is in Delivery
                req.status = 'Completed'
                req.save()
        except EquipmentInspection.DoesNotExist:
            pass
    
    return render(request, 'pages/internal_requests/motorpool_received_requests.html', {
        'sales_requests': sales_requests
    })


@login_required
@user_passes_test(is_motorpool)
@require_http_methods(["GET"])
def motorpool_received_requests_feed(request):
    """Return latest motorpool received requests as JSON for AJAX polling."""
    sales_requests = Request.objects.filter(
        request_type='PDI',
        assigned_to='Motorpool'
    ).order_by('-created_at')[:100]

    results = []
    for req in sales_requests:
        results.append({
            'id': req.id,
            'request_id': req.request_id,
            'request_type': req.request_type,
            'unit': req.unit,
            'invoice_number': req.invoice_number,
            'requested_by_name': req.requested_by_name,
            'status': req.status,
            'created_at': req.created_at.isoformat(),
        })

    return JsonResponse({'requests': results})


@login_required
@user_passes_test(is_motorpool)
def motorpool_sent_requests(request):
    return render(request, 'pages/internal_requests/motorpool_sent_requests.html')


@login_required
@user_passes_test(is_motorpool)
def motorpool_equipment_inspection(request):
    # Get all equipment inspections with related data
    inspections = EquipmentInspection.objects.select_related(
        'pdi_request'
    ).order_by('-created_at')
    
    print("\nProcessing equipment inspections:")
    
    # Get invoice data for each inspection's PDI request
    for inspection in inspections:
        print(f"\nInspection ID: {inspection.inspection_id}")
        print(f"PDI Request: {inspection.pdi_request}")
        
        try:
            # Get the invoice and its related data using inspection's invoice_number
            invoice = Invoice.objects.select_related(
                'order'
            ).prefetch_related(
                'order__items',
                'order__items__inventory_item'
            ).get(invoice_number=inspection.invoice_number)
            
            print(f"Found invoice: {invoice}")
            print(f"Order: {invoice.order}")
            print(f"Order items: {list(invoice.order.items.all()) if invoice.order else 'No order items'}")
            
            # Attach the invoice to the inspection for template access
            inspection.invoice = invoice
            
            # Check if delivery request exists using request_id
            inspection.has_delivery_request = DeliveryRequest.objects.filter(
                pdi_request_id=inspection.pdi_request.request_id
            ).exists()
            
            print(f"Has delivery request: {inspection.has_delivery_request}")
            print(f"Client info: {invoice.order.client_name if invoice.order else 'No client info'}")
            
        except Invoice.DoesNotExist:
            print(f"Invoice not found for number: {inspection.invoice_number}")
            inspection.invoice = None
            inspection.has_delivery_request = False
        except Exception as e:
            print(f"Error processing inspection: {str(e)}")
            print(f"Exception type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            inspection.invoice = None
            inspection.has_delivery_request = False
    
    return render(request, 'pages/equipment_inspection.html', {
        'inspections': inspections,
        'MEDIA_URL': settings.MEDIA_URL,
    })


@login_required
@user_passes_test(is_motorpool)
def motorpool_settings(request):
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
            return redirect('motorpool_settings')
    
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
    
    return render(request, 'pages/motorpool_settings.html', context)


@login_required
@user_passes_test(is_motorpool)
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


@login_required
@user_passes_test(is_motorpool)
@require_http_methods(["POST"])
def update_request_status(request):
    try:
        data = json.loads(request.body)
        request_id = data.get('request_id')
        new_status = data.get('status')
        
        if not new_status:
            return JsonResponse({
                'status': 'error',
                'message': 'Status cannot be empty'
            }, status=400)
        
        # Get the request object
        req = Request.objects.get(id=request_id)
        
        # Update status
        req.status = new_status
        req.save()
        
        # Add a note about the status change
        RequestNote.objects.create(
            request=req,
            note=f'Status updated to: {new_status}',
            created_by=request.user
        )

        # If status is changed to In Progress, create an equipment inspection record
        if new_status == 'In Progress':
            # Generate inspection ID
            date_str = datetime.now().strftime('%Y%m%d')
            last_inspection = EquipmentInspection.objects.filter(
                inspection_id__startswith=f'INS-{date_str}'
            ).order_by('inspection_id').last()
            
            if last_inspection:
                last_number = int(last_inspection.inspection_id.split('-')[-1])
                new_number = str(last_number + 1).zfill(4)
            else:
                new_number = '0001'
            
            inspection_id = f'INS-{date_str}-{new_number}'
            
            # Create inspection record
            EquipmentInspection.objects.create(
                inspection_id=inspection_id,
                request_type='PDI',
                unit=req.unit,
                date_received=datetime.now(),
                assigned_technician=None,  # Initially empty, to be assigned later
                status='Pending',
                pdi_request=req,  # Link to the original PDI request
                invoice_number=req.invoice_number
            )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Status updated successfully'
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


@login_required
@user_passes_test(is_motorpool)
@require_http_methods(["POST"])
def update_inspection(request):
    try:
        inspection_id = request.POST.get('inspection_id')
        inspection = EquipmentInspection.objects.get(id=inspection_id)
        
        # Update assigned technician as plain text
        technician_name = request.POST.get('assigned_technician', '').strip()
        if technician_name:
            inspection.assigned_technician = technician_name
            # If technician is assigned and status is Pending, change to In Progress
            if inspection.status == 'Pending':
                inspection.status = 'In Progress'
        
        # Update status if provided
        new_status = request.POST.get('status')
        if new_status:
            inspection.status = new_status
        
        # Handle checklist reference file
        if 'checklist_reference' in request.FILES:
            checklist_file = request.FILES['checklist_reference']
            file_name = f'inspections/{inspection_id}/checklist_{checklist_file.name}'
            if inspection.checklist_reference:
                # Delete old file if it exists
                inspection.checklist_reference.delete(save=False)
            inspection.checklist_reference = default_storage.save(file_name, checklist_file)
        
        # Handle assistants - parse JSON string into list
        assistants_json = request.POST.get('assisted_by')
        try:
            if assistants_json:
                assistants = json.loads(assistants_json)
                # Filter out empty strings and strip whitespace
                inspection.assisted_by = [name.strip() for name in assistants if name.strip()]
            else:
                inspection.assisted_by = []
        except json.JSONDecodeError:
            inspection.assisted_by = []
        
        # Handle Results & Findings fields
        inspection.inspection_result = request.POST.get('inspection_result')
        inspection.issues_found = request.POST.get('issues_found')
        inspection.corrective_actions = request.POST.get('corrective_actions')
        inspection.spare_parts_used = request.POST.get('spare_parts_used')
        inspection.notes = request.POST.get('notes')
        
        # Handle signed form
        if 'signed_form' in request.FILES:
            signed_form = request.FILES['signed_form']
            file_name = f'inspections/{inspection_id}/signed_form_{signed_form.name}'
            if inspection.signed_form:
                # Delete old file if it exists
                inspection.signed_form.delete(save=False)
            inspection.signed_form = default_storage.save(file_name, signed_form)
        
        # Handle inspection photos
        photos = []
        
        # Get existing photos that weren't removed
        existing_photos_json = request.POST.get('existing_photos', '[]')
        try:
            existing_photos = json.loads(existing_photos_json)
            # Clean up the paths and remove duplicates
            photos.extend(list(set([path.lstrip('/') for path in existing_photos])))
        except json.JSONDecodeError:
            pass
        
        # Handle new photos
        new_photos = []
        for key in request.FILES:
            if key.startswith('inspection_photo_'):
                photo = request.FILES[key]
                # Generate a unique filename using timestamp
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                file_name = f'inspections/{inspection_id}/photos/{timestamp}_{photo.name}'
                # Save the file and get the full URL
                saved_path = default_storage.save(file_name, photo)
                # Store the relative path
                new_photos.append(saved_path)
        
        # Ensure we don't exceed 3 photos total
        total_photos = photos + new_photos
        if len(total_photos) > 3:
            total_photos = total_photos[:3]
        
        # Update inspection photos
        inspection.inspection_photos = total_photos
        
        inspection.save()
        
        # Prepare full URLs for the response
        photo_urls = [f'{settings.MEDIA_URL}{photo}' for photo in total_photos]
        
        return JsonResponse({
            'status': 'success',
            'message': 'Inspection updated successfully',
            'photos': photo_urls,  # Return the full URLs
            'inspection_status': inspection.status,  # Return the updated status
            'assisted_by': inspection.assisted_by  # Return the updated assistants list
        })
    except EquipmentInspection.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Inspection not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@login_required
@user_passes_test(is_motorpool)
@require_http_methods(["POST"])
def send_to_delivery(request):
    try:
        data = json.loads(request.body)
        inspection_id = data.get('inspection_id')
        pdi_request_id = data.get('pdi_request_id')
        invoice_number = data.get('invoice_number')
        unit_info = data.get('unit_info', {})
        client_info = data.get('client_info', {})

        print("\nReceived data for delivery request:")
        print(f"Inspection ID: {inspection_id}")
        print(f"PDI Request ID: {pdi_request_id}")
        print(f"Invoice number: {invoice_number}")
        print(f"Unit info: {unit_info}")
        print(f"Client info: {client_info}")

        if not all([inspection_id, pdi_request_id, invoice_number]):
            return JsonResponse({
                'status': 'error',
                'message': 'Missing required data'
            }, status=400)

        # Get the inspection with related PDI request
        inspection = EquipmentInspection.objects.select_related('pdi_request').get(id=inspection_id)
        
        if not inspection.pdi_request:
            return JsonResponse({
                'status': 'error',
                'message': 'No PDI request found for this inspection'
            }, status=400)
        
        # Check if delivery request already exists using request_id
        existing_request = DeliveryRequest.objects.filter(pdi_request_id=inspection.pdi_request.request_id).first()
        if existing_request:
            return JsonResponse({
                'status': 'error',
                'message': 'A delivery request already exists for this inspection.',
                'exists': True
            })

        # Get the invoice and related data
        try:
            # Use inspection's invoice_number to get the invoice
            invoice = Invoice.objects.select_related(
                'order'
            ).prefetch_related(
                'order__items',
                'order__items__inventory_item'
            ).get(invoice_number=inspection.invoice_number)

            if not invoice.order:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No order found for this invoice'
                }, status=400)

            print(f"\nFound invoice: {invoice}")
            print(f"Order: {invoice.order}")
            print(f"Client info from invoice: {invoice.order.client_name}")

            # Get client info from the invoice's order
            client_info = {
                'client_name': invoice.order.client_name,
                'client_address': invoice.order.client_address,
                'client_contact': invoice.order.client_contact,
                'client_email': invoice.order.client_email,
                'company_name': invoice.order.company_name,
                'company_address': invoice.order.company_address,
                'company_contact': invoice.order.company_contact,
                'company_email': invoice.order.company_email
            }

            # Get unit info from the invoice's order items
            unit_item = invoice.order.items.first()
            if unit_item:
                unit_info = {
                    'unit_name': unit_item.inventory_item.unit_item,
                    'serial_number': unit_item.inventory_item.serial_number
                }

            # Create delivery request with data from invoice
            delivery_request = DeliveryRequest.objects.create(
                pdi_request_id=inspection.pdi_request.request_id,
                invoice_number=inspection.invoice_number,
                unit_info=unit_info,
                client_info=client_info,
                status='Pending'
            )

            print(f"Created delivery request: {delivery_request.request_id}")
            print(f"With client info: {delivery_request.client_info}")

            # Create notification for delivery department
            create_notification(
                title='New Delivery Request',
                message=f'New delivery request ({delivery_request.request_id}) for unit {unit_info.get("unit_name")} from Motorpool Department',
                notification_type='delivery_request',
                from_dept='motorpool',
                to_dept='delivery',
                related_id=delivery_request.id,
                related_link=f'/delivery/requests/?request_id={delivery_request.request_id}'
            )

            # Update inspection status
            inspection.status = 'Delivery'
            inspection.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Delivery request created successfully',
                'request_id': delivery_request.request_id
            })

        except Invoice.DoesNotExist:
            print(f"Invoice not found for number: {inspection.invoice_number}")
            return JsonResponse({
                'status': 'error',
                'message': 'Invoice not found for this inspection'
            }, status=404)
        except Exception as e:
            print(f"Error creating delivery request: {str(e)}")
            print(f"Exception type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return JsonResponse({
                'status': 'error',
                'message': f'Error creating delivery request: {str(e)}'
            }, status=500)

    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        print(f"Exception type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@login_required
@user_passes_test(is_motorpool)
def check_delivery_exists(request):
    inspection_id = request.GET.get('inspection_id')
    try:
        inspection = EquipmentInspection.objects.get(id=inspection_id)
        exists = DeliveryRequest.objects.filter(
            pdi_request_id=inspection.pdi_request.request_id
        ).exists()
        return JsonResponse({'exists': exists})
    except EquipmentInspection.DoesNotExist:
        return JsonResponse({'exists': False})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


