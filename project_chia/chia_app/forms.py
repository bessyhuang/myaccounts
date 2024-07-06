from django.forms import ModelForm, TextInput, Select
from datetime import date
from .models import Record

class RecordForm(ModelForm):
    class Meta:
        model = Record
        # fields = ['date', 'description', 'category', 'cash', 'balance_type']
        fields = "__all__"
		
        widgets = {
            'date': TextInput(
                attrs = {
                    'id': 'datepicker1', 
                    'value': date.today().strftime('%Y-%m-%d'),
                    'class': 'form-control'
                }
            ),
            'description': TextInput(
                attrs = {
                    'class': 'form-control'
                }
            ),
            'category': Select(
                attrs = {
                    'class': 'dropdown-item'
                }
            ),
            'cash': TextInput(
                attrs = {
                    'class': 'form-control'
                }
            ),
            'balance_type': Select(
                attrs = {
                    'class': 'dropdown-item'
                }
            )
        }

