from django.db import models
from adminpanel.models import InventoryItem
from django.utils import timezone
import uuid
from django.contrib.auth.models import User

class SalesOrder(models.Model):
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
    id_attachment = models.FileField(upload_to='sales_orders/ids/', blank=True, null=True)
    business_permit = models.FileField(upload_to='sales_orders/permits/', blank=True, null=True)
    bir_attachment = models.FileField(upload_to='sales_orders/bir/', blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Link to ClientRecord
    client_record = models.ForeignKey('ClientRecord', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')

    def __str__(self):
        return f"{self.order_number} - {self.client_name}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate order number: ORD-YYYYMMDD-XXXX
            date_str = timezone.now().strftime('%Y%m%d')
            last_order = SalesOrder.objects.filter(order_number__startswith=f'ORD-{date_str}').order_by('order_number').last()
            
            if last_order:
                last_number = int(last_order.order_number.split('-')[-1])
                new_number = str(last_number + 1).zfill(4)
            else:
                new_number = '0001'
            
            self.order_number = f'ORD-{date_str}-{new_number}'
        
        super().save(*args, **kwargs)

    @property
    def remaining_balance(self):
        """Calculate the remaining balance to be paid"""
        return self.total_amount - self.amount_paid

    @property
    def item_description(self):
        # Return a summary of items in the order, e.g. "2x Excavator, 1x Loader"
        items = self.items.select_related('inventory_item').all()
        if not items:
            return "-"
        return ', '.join(f"{item.quantity}x {item.inventory_item.unit_item}" for item in items)

class OrderItem(models.Model):
    order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items')
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.order.order_number} - {self.inventory_item.unit_item}"
    
    def save(self, *args, **kwargs):
        # Calculate total price
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

class Invoice(models.Model):
    INVOICE_STATUS = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Overdue', 'Overdue'),
        ('Cancelled', 'Cancelled'),
    )

    invoice_number = models.CharField(max_length=20, unique=True)
    order = models.OneToOneField('SalesOrder', on_delete=models.CASCADE, related_name='invoice')
    client_name = models.CharField(max_length=255)
    department = models.CharField(max_length=100, default='Sales')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=INVOICE_STATUS, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Link to ClientRecord
    client_record = models.ForeignKey('ClientRecord', on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Generate invoice number: INV-YEAR-SEQUENTIAL
            year = timezone.now().strftime('%y')
            last_invoice = Invoice.objects.filter(invoice_number__startswith=f'INV-{year}').order_by('invoice_number').last()
            
            if last_invoice:
                last_number = int(last_invoice.invoice_number.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
                
            self.invoice_number = f'INV-{year}-{new_number:04d}'
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_number

class Request(models.Model):
    request_id = models.CharField(max_length=20, unique=True)
    request_type = models.CharField(max_length=50)
    unit = models.CharField(max_length=100)
    invoice_number = models.CharField(max_length=50)
    invoice_id = models.CharField(max_length=50)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    requested_by_name = models.CharField(max_length=255, blank=True)
    assigned_to = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='Pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.requested_by_name and self.requested_by:
            self.requested_by_name = f"{self.requested_by.first_name} {self.requested_by.last_name}".strip() or self.requested_by.username
        if not self.request_id:
            # Generate request ID: REQ-YYYYMMDD-XXXX
            date_str = timezone.now().strftime('%Y%m%d')
            last_request = Request.objects.filter(request_id__startswith=f'REQ-{date_str}').order_by('request_id').last()
            
            if last_request:
                last_number = int(last_request.request_id.split('-')[-1])
                new_number = str(last_number + 1).zfill(4)
            else:
                new_number = '0001'
            
            self.request_id = f'REQ-{date_str}-{new_number}'
        
        super().save(*args, **kwargs)

class RequestNote(models.Model):
    request = models.ForeignKey('Request', on_delete=models.CASCADE, related_name='note_history')
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Note for {self.request.request_id} at {self.created_at}"

class ClientRecord(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    client_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    contact_info = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()
    total_orders = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    last_order_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Link to the delivery that created this record
    delivery_schedule = models.ForeignKey('delivery.DeliverySchedule', on_delete=models.SET_NULL, null=True, blank=True)
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.client_name} - {self.company_name or 'No Company'}"

    class Meta:
        ordering = ['-last_order_date']
