"""前端表單的顯示"""
from datetime import date

from django.forms import ModelForm, TextInput, Select
from .models import Record

class RecordForm(ModelForm):
    """Form: 收支紀錄"""    
    class Meta:
        """設定欄位於前端的顯示（widgets）"""
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
            'description': TextInput(attrs = {'class': 'form-control'}),
            'category': Select(attrs = {'class': 'dropdown-item'}),
            'cash': TextInput(attrs = {'class': 'form-control'}),
            'balance_type': Select(attrs = {'class': 'dropdown-item'})
        }
