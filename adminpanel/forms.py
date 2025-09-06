from django import forms
from .models import InventoryItem, UserSettings

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = [
            'category', 'unit_item', 'details', 'supplier', 'quantity', 
            'unit_price', 'date_received', 'department', 'photo', 'serial_number'
        ]
        widgets = {
            'date_received': forms.DateInput(attrs={'type': 'date'}),
            'details': forms.Textarea(attrs={'rows': 3}),
        }

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = ['timezone', 'date_format']
        widgets = {
            'timezone': forms.Select(attrs={'class': 'form-select flex-grow-1 ms-3 fields'}),
            'date_format': forms.Select(attrs={'class': 'form-select flex-grow-1 ms-4 fields'}),
        }
