from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('pdi_request', 'PDI Request'),
        ('delivery_request', 'Delivery Request'),
        ('inspection_complete', 'Inspection Complete'),
        ('delivery_complete', 'Delivery Complete'),
        ('payment_received', 'Payment Received'),
        ('order_created', 'Order Created'),
        ('invoice_generated', 'Invoice Generated'),
    ]

    DEPARTMENTS = [
        ('sales', 'Sales'),
        ('motorpool', 'Motorpool'),
        ('warehouse', 'Warehouse'),
        ('delivery', 'Delivery'),
        ('aftersales', 'Aftersales'),
        ('admin', 'Admin'),
    ]

    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    from_department = models.CharField(max_length=50, choices=DEPARTMENTS)
    to_department = models.CharField(max_length=50, choices=DEPARTMENTS)
    created_at = models.DateTimeField(default=timezone.now)
    read_by = models.ManyToManyField(User, related_name='read_notifications', blank=True)
    related_id = models.IntegerField(null=True, blank=True)  # Store related record ID (order_id, invoice_id, etc.)
    related_link = models.CharField(max_length=255, blank=True)  # Store URL to related content

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - From: {self.from_department} To: {self.to_department}"

    def mark_as_read(self, user):
        self.read_by.add(user)
        self.save()

    @property
    def is_read(self, user):
        return self.read_by.filter(id=user.id).exists()
