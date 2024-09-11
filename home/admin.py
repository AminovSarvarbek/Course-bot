# home/admin.py

from django.contrib import admin
from .models import *

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Dars jadvali uchun (yani dars kunlari)
@admin.register(Lesson_table)
class LessonTableAdmin(admin.ModelAdmin):
    list_display = ('guruh', 'lesson_date', 'start_time', 'end_time')
    list_filter = ('guruh', 'lesson_date')
    search_fields = ('guruh__name', 'lesson_date')