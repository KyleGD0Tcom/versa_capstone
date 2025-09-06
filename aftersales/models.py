from django.db import models
from django.utils import timezone
from sales.models import SalesOrder, Invoice
from delivery.models import DeliverySchedule

class ServiceRecord(models.Model):
    STATUS_CHOICES = [
        ('Warranty Active', 'Warranty Active'),
        ('Warranty Expired', 'Warranty Expired'),
        ('No Warranty', 'No Warranty'),
    ]

    WARRANTY_TYPE_CHOICES = [
        ('Dump Truck', 'Dump Truck'),
        ('Heavy Equipment', 'Heavy Equipment'),
    ]

    service_id = models.CharField(max_length=20, unique=True)
    unit_name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=100)
    client_name = models.CharField(max_length=255)
    warranty_start = models.DateField()
    warranty_end = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Warranty Active')
    warranty_type = models.CharField(max_length=20, choices=WARRANTY_TYPE_CHOICES)
    usage_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # For tracking km or hours
    usage_unit = models.CharField(max_length=10, default='km')  # 'km' for dump trucks, 'hrs' for heavy equipment
    
    # Links to related records
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.SET_NULL, null=True, related_name='service_records')
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, related_name='service_records')
    delivery_schedule = models.ForeignKey(DeliverySchedule, on_delete=models.SET_NULL, null=True, related_name='service_records')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.service_id:
            # Generate service_id if not set (format: AS-YY-XXXX)
            last_record = ServiceRecord.objects.order_by('-service_id').first()
            if last_record and last_record.service_id:
                last_number = int(last_record.service_id.split('-')[-1])
                new_number = str(last_number + 1).zfill(4)
            else:
                new_number = '0001'
            
            year = timezone.now().strftime('%y')
            self.service_id = f'AS-{year}-{new_number}'

        # Set warranty type and usage unit based on unit name
        if not self.warranty_type or self.warranty_type not in dict(self.WARRANTY_TYPE_CHOICES):
            if 'dump truck' in self.unit_name.lower():
                self.warranty_type = 'Dump Truck'
                self.usage_unit = 'km'
            else:
                self.warranty_type = 'Heavy Equipment'
                self.usage_unit = 'hrs'

        # Check warranty status
        self.check_warranty_status()
        
        super().save(*args, **kwargs)

    def check_warranty_status(self):
        """Check if warranty is still valid based on time and usage"""
        now = timezone.now().date()
        
        # Check time-based warranty
        if now > self.warranty_end:
            self.status = 'Warranty Expired'
            return

        # Check usage-based warranty
        if self.warranty_type == 'Dump Truck' and self.usage_value >= 2000:
            self.status = 'Warranty Expired'
            return
        elif self.warranty_type == 'Heavy Equipment' and self.usage_value >= 2000:
            self.status = 'Warranty Expired'
            return

        self.status = 'Warranty Active'

    def __str__(self):
        return self.service_id

    class Meta:
        ordering = ['-created_at']

class Technician(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MaintenanceRecord(models.Model):
    maintenance_id = models.CharField(max_length=20, primary_key=True)
    service_record = models.ForeignKey(ServiceRecord, on_delete=models.CASCADE, related_name='maintenance_records', null=True)
    service_id = models.CharField(max_length=20)  # Keep temporarily for migration
    unit_name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=50)
    client_name = models.CharField(max_length=100)
    technicians = models.ManyToManyField(Technician, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('On Hold', 'On Hold'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ], default='Pending')
    reported_problem = models.TextField(null=True, blank=True)
    diagnosis = models.TextField(null=True, blank=True)
    findings_note = models.TextField(null=True, blank=True)
    work_performed = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.service_id and not self.service_record:
            try:
                self.service_record = ServiceRecord.objects.get(service_id=self.service_id)
            except ServiceRecord.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return self.maintenance_id
