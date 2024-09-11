from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import re


# Validation for phone numbers
def validate_phone_number(value):
    # Convert integer to string for validation
    value_str = str(value)
    pattern = r'^998\d{7}$'
    if not re.match(pattern, value_str) or len(value_str) != 10:
        raise ValidationError(
            'Telefon raqami 998 bilan boshlanishi, 10 ta raqamdan iborat bo\'lishi kerak.'
        )

# Models
class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Dars jadvali uchun (yani dars kunlari)
class WeekDay(models.TextChoices):
    DUSHANBA = 'Dushanba', 'Dushanba'
    SESHANBA = 'Seshanba', 'Seshanba'
    CHORSHANBA = 'Chorshanba', 'Chorshanba'
    PAYSHANBA = 'Payshanba', 'Payshanba'
    JUMA = 'Juma', 'Juma'
    SHANBA = 'Shanba', 'Shanba'
    YAKSHANBA = 'Yakshanba', 'Yakshanba'

class Lesson_table(models.Model):
    guruh = models.ForeignKey(Group, on_delete=models.CASCADE)
    lesson_date = models.CharField(max_length=10, choices=WeekDay.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()


    def clean(self):
        super().clean()
    
    # Tekshirish uchun start_time va end_time qiymatlari mavjudligini tekshiring
        if self.start_time is not None and self.end_time is not None:
            if self.start_time >= self.end_time:
                raise ValidationError('End time must be after start time.')

    def __str__(self):
        return f"{self.guruh.name}"