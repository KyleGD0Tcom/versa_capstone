from django.db.models.signals import post_save
from django.dispatch import receiver
from delivery.models import DeliverySchedule
from .models import ServiceRecord
from sales.models import Invoice
from datetime import timedelta
import logging
import traceback

logger = logging.getLogger(__name__)

@receiver(post_save, sender=DeliverySchedule)
def create_service_record_on_delivery(sender, instance, created, **kwargs):
    """
    Signal to create a service record when a delivery is marked as delivered
    """
    logger.info(f"Signal triggered for DeliverySchedule {instance.schedule_id}")
    logger.info(f"Status: {instance.status}")
    logger.info(f"Created: {created}")
    logger.info(f"Delivery request: {instance.delivery_request.request_id}")
    logger.info(f"Delivery request invoice number: {instance.delivery_request.invoice_number}")
    
    if instance.status == 'Delivered':
        # Only for sales deliveries, not warehouse
        invoice_number = instance.delivery_request.invoice_number
        if invoice_number.startswith('INVWH-'):
            return  # Do not create service record for warehouse deliveries
        try:
            logger.info(f"Processing delivered schedule {instance.schedule_id}")
            
            # Try to get the invoice and order, but allow them to be None
            invoice = None
            order = None
            try:
                invoice = Invoice.objects.get(invoice_number=instance.delivery_request.invoice_number)
                order = getattr(invoice, 'order', None)
                logger.info(f"Found invoice {invoice.invoice_number} and order {getattr(order, 'order_number', None)}")
            except Invoice.DoesNotExist:
                logger.warning(f"Invoice not found for number: {instance.delivery_request.invoice_number}. Service record will be created with invoice=None.")
            except Exception as e:
                logger.warning(f"Error getting invoice/order: {str(e)}. Service record will be created with invoice/order=None.")
                logger.warning(traceback.format_exc())
            
            # Get unit info from delivery request
            unit_info = instance.delivery_request.unit_info or {}
            client_info = instance.delivery_request.client_info or {}
            logger.info(f"Unit info: {unit_info}")
            logger.info(f"Client info: {client_info}")
            
            # Calculate warranty dates (assuming 1 year warranty from delivery date)
            warranty_start = instance.delivery_date
            warranty_end = warranty_start + timedelta(days=365)
            logger.info(f"Warranty dates: {warranty_start} to {warranty_end}")
            
            # Check if service record already exists
            if ServiceRecord.objects.filter(delivery_schedule=instance).exists():
                logger.info(f"Service record already exists for delivery schedule {instance.schedule_id}")
                return
            
            # Create service record even if invoice/order is None
            try:
                service_record = ServiceRecord.objects.create(
                    unit_name=unit_info.get('unit_name', ''),
                    serial_number=unit_info.get('serial_number', ''),
                    client_name=client_info.get('client_name', ''),
                    warranty_start=warranty_start,
                    warranty_end=warranty_end,
                    status='Warranty Active',
                    sales_order=order,
                    invoice=invoice,
                    delivery_schedule=instance
                )
                logger.info(f"Created service record {service_record.service_id} for delivery schedule {instance.schedule_id}")
            except Exception as e:
                logger.error(f"Error creating service record: {str(e)}")
                logger.error(traceback.format_exc())
        except Exception as e:
            logger.error(f"Error in signal: {str(e)}")
            logger.error(traceback.format_exc()) 