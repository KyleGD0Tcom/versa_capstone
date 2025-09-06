from django.db import models
from adminpanel.models import InventoryItem
from django.utils import timezone
from django.contrib.auth.models import User
from decimal import Decimal

class WarehouseOrder(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    PAYMENT_MODE_CHOICES = [
        ('cash', 'Cash'),
        ('inhouse', 'In-house'),
        ('financing', 'Financing'),
        ('loan', 'Loan'),
    ]

    order_number = models.CharField(max_length=20, unique=True)
    
    # Client Information
    client_name = models.CharField(max_length=255)
    client_address = models.TextField()
    client_contact = models.CharField(max_length=100)
    client_email = models.EmailField()
    
    # Company Information
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_address = models.TextField(blank=True, null=True)
    company_contact = models.CharField(max_length=100, blank=True, null=True)
    company_email = models.EmailField(blank=True, null=True)
    
    order_date = models.DateField(default=timezone.now)
    delivery_date = models.DateField()
    delivery_instructions = models.TextField(blank=True)
    
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE_CHOICES)
    due_date = models.DateField()
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Fields for non-cash payments
    residence_location = models.TextField(blank=True, null=True)
    bank_account = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=100, blank=True, null=True)
    
    # Attachments
    id_attachment = models.FileField(upload_to='warehouse_orders/ids/', blank=True, null=True)
    business_permit = models.FileField(upload_to='warehouse_orders/permits/', blank=True, null=True)
    bir_attachment = models.FileField(upload_to='warehouse_orders/bir/', blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.order_number} - {self.client_name}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate order number: ORDWH-YYYYMMDD-XXXX
            date_str = timezone.now().strftime('%Y%m%d')
            last_order = WarehouseOrder.objects.filter(order_number__startswith=f'ORDWH-{date_str}').order_by('order_number').last()
            
            if last_order:
                last_number = int(last_order.order_number.split('-')[-1])
                new_number = str(last_number + 1).zfill(4)
            else:
                new_number = '0001'
            
            self.order_number = f'ORDWH-{date_str}-{new_number}'
        
        super().save(*args, **kwargs)

    @property
    def remaining_balance(self):
        """Calculate the remaining balance to be paid"""
        return self.total_amount - self.amount_paid

class WarehouseOrderItem(models.Model):
    order = models.ForeignKey(WarehouseOrder, on_delete=models.CASCADE, related_name='items')
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    item_code = models.CharField(max_length=100, blank=True, null=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.order.order_number} - {self.inventory_item.unit_item}"
    
    def save(self, *args, **kwargs):
        # Calculate total price
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

class WarehouseInvoice(models.Model):
    order = models.OneToOneField(WarehouseOrder, on_delete=models.CASCADE, related_name='invoice')
    invoice_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, default='Pending')
    invoice_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.invoice_number

class WarehouseClientRecord(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    
    client_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    contact_info = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    total_orders = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    last_order_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Link to the delivery that created this record
    delivery_schedule = models.ForeignKey('delivery.DeliverySchedule', on_delete=models.SET_NULL, null=True, blank=True)
    warehouse_order = models.ForeignKey('WarehouseOrder', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.client_name} - {self.company_name or 'No Company'}"

    class Meta:
        ordering = ['-last_order_date']
