from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  # Correct import

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    work_shift = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    employee_type = models.CharField(max_length=50, null=True, blank=True)
    plain_password = models.CharField(max_length=255, blank=True, null=True)
    date_of_joining = models.DateTimeField(default=timezone.now)  # Correct usage of timezone.now
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=50, default='UTC+08:00')  # Default to Manila timezone
    date_format = models.CharField(max_length=20, default='MM/DD/YYYY')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Settings for {self.user.username}"

    class Meta:
        verbose_name_plural = "User Settings"


import random
import string
from django.db import models

class InventoryItem(models.Model):
    CATEGORY_CHOICES = [
        ('Heavy Equipment', 'Heavy Equipment'),
        ('Spare Parts', 'Spare Parts'),
    ]

    DEPARTMENT_CHOICES = [
        ('Warehouse', 'Warehouse'),
        ('Sales', 'Sales'),
    ]
    
    item_code = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    unit_item = models.CharField(max_length=255)
    details = models.TextField()
    supplier = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_received = models.DateField()
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)  # 👈 NEW FIELD
    photo = models.ImageField(upload_to='inventory_photos/', null=True, blank=True)
    serial_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.item_code} - {self.unit_item}'
    
    def save(self, *args, **kwargs):
        if not self.item_code:
            self.item_code = self.generate_item_code()
            while InventoryItem.objects.filter(item_code=self.item_code).exists():
                self.item_code = self.generate_item_code()
        super().save(*args, **kwargs)

    def generate_item_code(self):
        prefix = 'HVY-' if self.category == 'Heavy Equipment' else 'SP-'
        random_string = ''.join(random.choices(string.digits, k=6))
        return prefix + random_string
