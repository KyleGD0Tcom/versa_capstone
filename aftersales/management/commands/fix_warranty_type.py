from django.core.management.base import BaseCommand
from aftersales.models import ServiceRecord

class Command(BaseCommand):
    help = 'Fix ServiceRecord warranty_type values from Other to Dump Truck or Heavy Equipment.'

    def handle(self, *args, **kwargs):
        updated = 0
        for record in ServiceRecord.objects.filter(warranty_type='Other'):
            if 'dump truck' in record.unit_name.lower():
                record.warranty_type = 'Dump Truck'
                record.usage_unit = 'km'
            else:
                record.warranty_type = 'Heavy Equipment'
                record.usage_unit = 'hrs'
            record.save()
            updated += 1
        self.stdout.write(self.style.SUCCESS(f'Updated {updated} ServiceRecord(s) warranty_type from Other.')) 