from django.core.management.base import BaseCommand
from delivery.models import DeliverySchedule
from sales.models import ClientRecord

class Command(BaseCommand):
    help = 'Backfill client records for existing delivered schedules'

    def handle(self, *args, **kwargs):
        delivered_schedules = DeliverySchedule.objects.filter(status='Delivered')
        created_count = 0
        updated_count = 0

        for schedule in delivered_schedules:
            client_info = schedule.delivery_request.client_info
            
            try:
                client_record = ClientRecord.objects.get(
                    client_name=client_info.get('client_name'),
                    contact_info=client_info.get('client_contact')
                )
                # Update existing record
                client_record.total_orders += 1
                client_record.last_order_date = schedule.delivery_date
                client_record.save()
                updated_count += 1
            except ClientRecord.DoesNotExist:
                # Create new client record
                ClientRecord.objects.create(
                    client_name=client_info.get('client_name'),
                    company_name=client_info.get('company_name'),
                    contact_info=client_info.get('client_contact'),
                    email=client_info.get('client_email'),
                    address=client_info.get('client_address'),
                    delivery_schedule=schedule,
                    status='Active'
                )
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully processed {delivered_schedules.count()} delivered schedules: '
                f'{created_count} new records created, {updated_count} existing records updated'
            )
        ) 