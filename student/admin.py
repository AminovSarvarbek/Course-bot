from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'group', 'phone', 'start_date','amount','school_name','student_class','is_active',)
    search_fields = ('first_name', 'last_name', 'phone')
    list_filter = ('group',)
