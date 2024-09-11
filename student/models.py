from django.db import models
from group.models import Group
from django.core.exceptions import ValidationError
from django.db import models
import re
# Xatolik berishi mumkin bo'lgan 
def validate_phone(value):
    pattern = r'^\+998\d{9}$'  # +998 bilan boshlanadi va keyin 9 ta raqam bo'ladi (jami 12 ta belgidan iborat)
    if not re.match(pattern, value):
        raise ValidationError("Telefon raqam +998 bilan boshlanishi va undan keyin 9 ta raqam bo‘lishi kerak.")


# Create your models here.
class Student(models.Model):
    first_name = models.CharField(max_length=25,blank=False)
    last_name = models.CharField(max_length=25,blank=False)
    father_name = models.CharField(max_length=25,blank=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE,null=False, blank=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=False, blank=False)
    school_name = models.CharField(max_length=25,blank=False)
    student_class = models.CharField(max_length=25,blank=False)
    phone = models.CharField(max_length=12, validators=[],blank=False,unique=True)
    start_date = models.DateField(null=False,blank=False)
    telegram_id = models.BigIntegerField(null=True, blank=True,unique=True)
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'students'
