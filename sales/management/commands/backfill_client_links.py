from django.core.management.base import BaseCommand
from sales.models import ClientRecord, SalesOrder, Invoice

class Command(BaseCommand):
    help = 'Backfill SalesOrder and Invoice client_record ForeignKey for all existing data'

    def handle(self, *args, **kwargs):
        updated_orders = 0
        updated_invoices = 0
        for client in ClientRecord.objects.all():
            # Link all orders for this client
            orders = SalesOrder.objects.filter(client_name__iexact=client.client_name.strip())
            updated_orders += orders.update(client_record=client)
            # Link all invoices for this client
            invoices = Invoice.objects.filter(client_name__iexact=client.client_name.strip())
            updated_invoices += invoices.update(client_record=client)
        self.stdout.write(self.style.SUCCESS(
            f'Linked {updated_orders} orders and {updated_invoices} invoices to their ClientRecords.'
        )) 