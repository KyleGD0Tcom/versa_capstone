from django.db import models
from django.contrib.auth.models import User
from sales.models import Request

# Create your models here.

class EquipmentInspection(models.Model):
    INSPECTION_RESULT_CHOICES = [
        ('Passed', 'Passed'),
        ('Failed', 'Failed'),
    ]

    inspection_id = models.CharField(max_length=20, unique=True)
    request_type = models.CharField(max_length=50)  # PDI, etc.
    unit = models.CharField(max_length=255)
    date_received = models.DateTimeField()
    assigned_technician = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=50)  # Pending, In Progress, Passed, Failed
    pdi_request = models.ForeignKey(Request, on_delete=models.SET_NULL, null=True, related_name='inspections')
    invoice_number = models.CharField(max_length=50)
    checklist_reference = models.FileField(upload_to='inspection_checklists/', null=True, blank=True)
    assisted_by = models.JSONField(null=True, blank=True, default=list)  # Store list of assistant names
    
    # Results & Findings fields
    inspection_result = models.CharField(max_length=20, choices=INSPECTION_RESULT_CHOICES, null=True, blank=True)
    issues_found = models.TextField(null=True, blank=True)
    corrective_actions = models.TextField(null=True, blank=True)
    spare_parts_used = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    # Attachments
    inspection_photos = models.JSONField(null=True, blank=True, default=list)  # Store list of photo paths
    signed_form = models.FileField(upload_to='inspection_signed_forms/', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.inspection_id

    class Meta:
        ordering = ['-created_at']
