import re
from django import forms
from django.core.exceptions import ValidationError

from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
        widgets = {
            'paid_months': forms.DateInput(attrs={'type': 'month'}, format='%Y-%m'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paid_months'].input_formats = ['%Y-%m']


    def clean_paid_months(self):
        paid_months = self.cleaned_data.get('paid_months')

        # YYYY-MM formatini tekshirish uchun regex
        if paid_months and not re.match(r'^\d{4}-(0[1-9]|1[0-2])$', paid_months):
            raise ValidationError("Please enter a valid year and month in the format YYYY-MM.")
        
        return paid_months

    # def clean(self):
    #     cleaned_data = super().clean()
    #     student = cleaned_data.get('student')
    #     amount = cleaned_data.get('amount')

    #     if student and student.amount != amount:
    #         raise ValidationError(
    #             "Student's amount and Payment's amount are not equal."
    #         )

    #     return cleaned_data


