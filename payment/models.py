from django.db import models
from student.models import Student
from django.utils import timezone
from django import forms

class YearMonthField(models.CharField):
    def formfield(self, **kwargs):
        defaults = {
            'widget': forms.DateInput(attrs={'type': 'month'}, format='%Y-%m'),
            'input_formats': ['%Y-%m'],
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)

class Payment(models.Model):
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE, blank=True)
    paid_months = models.CharField(max_length=7, null=True, blank=True)  # YYYY-MM format uchun
    payment_time = models.DateTimeField(null=True, default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'payment'

    def __str__(self):
        return f"{self.student}"

    # def save(self, *args, **kwargs):
    #     if self.student and self.student.amount == self.amount:
    #         super().save(*args, **kwargs)
    #     else:
    #         # Student.amount bilan amount teng bo'lmasa saqlanmaydi
    #         raise ValueError("Student's amount and Payment's amount are not equal.")