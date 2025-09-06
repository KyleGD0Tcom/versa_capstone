from django.db.models.signals import post_save
from django.dispatch import receiver
from delivery.models import DeliverySchedule
from .models import ClientRecord, SalesOrder

@receiver(post_save, sender=DeliverySchedule)
def create_client_record_on_delivery(sender, instance, created, **kwargs):
    """
    Signal to create or update a client record when a delivery is marked as delivered
    """
    if instance.status == 'Delivered':
        # Only for sales deliveries, not warehouse
        invoice_number = instance.delivery_request.invoice_number
        if invoice_number.startswith('INVWH-'):
            return  # Do not create/update client record for warehouse deliveries
        # Get client info from the delivery request
        client_info = instance.delivery_request.client_info
        
        # Try to find existing client record
        try:
            client_record = ClientRecord.objects.get(
                client_name=client_info.get('client_name'),
                contact_info=client_info.get('client_contact')
            )
            # Update existing record
            client_record.total_orders += 1
            client_record.last_order_date = instance.delivery_date
            client_record.save()
        except ClientRecord.DoesNotExist:
            # Create new client record
            client_record = ClientRecord.objects.create(
                client_name=client_info.get('client_name'),
                company_name=client_info.get('company_name'),
                contact_info=client_info.get('client_contact'),
                email=client_info.get('client_email'),
                address=client_info.get('client_address'),
                delivery_schedule=instance,
                status='Active'
            )
        # Link all related SalesOrder and Invoice records to this ClientRecord
        from sales.models import SalesOrder, Invoice
        SalesOrder.objects.filter(client_name__iexact=client_record.client_name.strip()).update(client_record=client_record)
        Invoice.objects.filter(client_name__iexact=client_record.client_name.strip()).update(client_record=client_record) 