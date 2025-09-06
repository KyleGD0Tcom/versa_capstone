from django import forms
from .models import MaintenanceRecord, Technician

class MaintenanceUpdateForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = [
            'reported_problem', 'diagnosis', 'findings_note', 'work_performed'
        ] 