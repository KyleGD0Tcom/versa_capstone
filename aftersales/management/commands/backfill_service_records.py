from django.core.management.base import BaseCommand
from delivery.models import DeliverySchedule
from aftersales.models import ServiceRecord
from datetime import timedelta
import traceback
from sales.models import Invoice

class Command(BaseCommand):
    help = 'Backfill service records for existing delivered schedules'

    def handle(self, *args, **kwargs):
        delivered_schedules = DeliverySchedule.objects.filter(status='Delivered')
        created_count = 0
        error_count = 0

        for schedule in delivered_schedules:
            try:
                # Check if service record already exists
                if ServiceRecord.objects.filter(delivery_schedule=schedule).exists():
                    continue

                # Get the invoice and order from the delivery request (allow missing)
                invoice = None
                order = None
                try:
                    invoice = Invoice.objects.get(invoice_number=schedule.delivery_request.invoice_number)
                    order = getattr(invoice, 'order', None)
                except Invoice.DoesNotExist:
                    print(f"Invoice not found for schedule {schedule.schedule_id} (invoice_number={schedule.delivery_request.invoice_number})")
                except Exception as e:
                    print(f"Error getting invoice/order for schedule {schedule.schedule_id}: {e}")
                    traceback.print_exc()

                # Get unit info from delivery request
                unit_info = schedule.delivery_request.unit_info or {}
                client_info = schedule.delivery_request.client_info or {}

                # Calculate warranty dates (assuming 1 year warranty from delivery date)
                warranty_start = schedule.delivery_date
                warranty_end = warranty_start + timedelta(days=365)

                # Create service record
                ServiceRecord.objects.create(
                    unit_name=unit_info.get('unit_name', ''),
                    serial_number=unit_info.get('serial_number', ''),
                    client_name=client_info.get('client_name', ''),
                    warranty_start=warranty_start,
                    warranty_end=warranty_end,
                    status='Warranty Active',
                    sales_order=order,
                    invoice=invoice,
                    delivery_schedule=schedule
                )
                created_count += 1
            except Exception as e:
                print(f"Error creating service record for schedule {schedule.schedule_id}: {str(e)}")
                traceback.print_exc()
                error_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully processed {delivered_schedules.count()} delivered schedules: '
                f'{created_count} new records created, {error_count} errors'
            )
        ) 