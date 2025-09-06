from django import forms
from .models import SalesOrder, OrderItem
from adminpanel.models import InventoryItem

class SalesOrderForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        fields = [
            'client_name', 'client_address', 'client_contact', 'client_email',
            'company_name', 'company_address', 'company_contact', 'company_email',
            'delivery_date', 'delivery_instructions', 'payment_mode', 'due_date',
            'amount_paid', 'residence_location', 'bank_account', 'account_number',
            'id_attachment', 'business_permit', 'bir_attachment'
        ]
        widgets = {
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class OrderItemForm(forms.ModelForm):
    item_name = forms.ModelChoiceField(
        queryset=InventoryItem.objects.filter(department='Sales'),
        empty_label="Select Item",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = OrderItem
        fields = ['item_name', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rename the field label
        self.fields['item_name'].label = "Item Name" 