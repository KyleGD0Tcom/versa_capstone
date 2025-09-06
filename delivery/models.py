from django.db import models
from django.utils import timezone

# Create your models here.

class DeliveryRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
    ]

    request_id = models.CharField(max_length=20, unique=True)
    pdi_request_id = models.CharField(max_length=50)
    invoice_number = models.CharField(max_length=50)
    unit_info = models.JSONField(default=dict, blank=True)
    client_info = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        if not self.request_id:
            # Generate request_id if not set (format: DVR-YYYY-XXXX)
            last_request = DeliveryRequest.objects.order_by('-request_id').first()
            if last_request and last_request.request_id:
                last_number = int(last_request.request_id.split('-')[-1])
                new_number = str(last_number + 1).zfill(4)
            else:
                new_number = '0001'
            
            year = timezone.now().strftime('%Y')
            self.request_id = f'DVR-{year}-{new_number}'
        
        # Ensure unit_info and client_info are dictionaries with default empty values
        if not self.unit_info:
            self.unit_info = {}
        if not self.client_info:
            self.client_info = {}
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.request_id

class DeliverySchedule(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('In-Transit', 'In-Transit'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    delivery_request = models.ForeignKey(DeliveryRequest, on_delete=models.CASCADE, related_name='schedules')
    schedule_id = models.CharField(max_length=20, unique=True)
    assigned_driver = models.CharField(max_length=100)
    delivery_date = models.DateField()
    delivery_instructions = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.schedule_id:
            # Generate schedule_id if not set (format: DVS-YYYY-XXXX)
            last_schedule = DeliverySchedule.objects.order_by('-schedule_id').first()
            if last_schedule and last_schedule.schedule_id:
                last_number = int(last_schedule.schedule_id.split('-')[-1])
                new_number = str(last_number + 1).zfill(4)
            else:
                new_number = '0001'
            
            year = timezone.now().strftime('%Y')
            self.schedule_id = f'DVS-{year}-{new_number}'
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.schedule_id
