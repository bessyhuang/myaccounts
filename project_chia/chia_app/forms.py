"""前端表單的顯示"""
from datetime import date

from django import forms

# from django.forms import ModelForm, TextInput, Select
from .models import Record


class RecordForm(forms.ModelForm):
    """Form: 收支紀錄"""

    def __init__(self, *args, **kwargs):
        """初始化"""
        super().__init__(*args, **kwargs)
        self.fields["balance_type"].initial = "支出"

    class Meta:  # pylint: disable=R0903
        """設定欄位於前端的顯示（widgets）"""

        model = Record
        # fields = ['date', 'description', 'category', 'cash', 'balance_type']
        fields = "__all__"
        widgets = {
            "date": forms.TextInput(
                attrs={
                    "id": "datepicker1",
                    "value": date.today().strftime("%Y-%m-%d"),
                    "class": "form-control",
                }
            ),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "dropdown-item"}),
            "cash": forms.TextInput(attrs={"class": "form-control"}),
            "balance_type": forms.Select(attrs={"class": "dropdown-item"}),
        }
