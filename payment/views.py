from datetime import date
from dateutil.relativedelta import relativedelta
from django.shortcuts import render
from django.db.models.functions import Concat
from django.db.models import Sum, F, Value
from django.utils import timezone

from payment.models import Payment
from student.models import Student
from group.models import Group
from .utils import get_students_with_unpaid_months


def unpaidPaymentsView(request):
    # Get the group name filter from the query parameters
    group_name = request.GET.get('group', None)
    
    # Fetch students with unpaid months, optionally filtering by group name
    unpaid_list = get_students_with_unpaid_months(group_name=group_name)
    
    # Fetch distinct group names for the filter dropdown
    groups = Group.objects.values_list('name', flat=True).distinct()
    
    return render(request, 'payment/unpaid.html', {
        'unpaid_list': unpaid_list,
        'groups': groups,
    })

def revenue_view(request):
    selected_group = request.GET.get('group', '')
    
    # Step 1: Aggregate total revenue from all payments
    total_revenue = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0

    # Step 2: Group students by their respective groups and calculate their individual revenue
    grouped_data = {}
    students = Student.objects.all()

    if selected_group:
        students = students.filter(group__name=selected_group)
    
    for student in students:
        # Calculate the revenue for each student
        student_revenue = Payment.objects.filter(student=student).aggregate(total=Sum('amount'))['total'] or 0

        # Group by student group, and store each student's name and revenue
        group_name = student.group.name if student.group else "Unknown Group"

        if group_name not in grouped_data:
            grouped_data[group_name] = []

        grouped_data[group_name].append({
            'student_name': student.first_name,
            'student_revenue': student_revenue
        })
    
    # Fetch all group names for the dropdown
    groups = Student.objects.values_list('group__name', flat=True).distinct()
    
    context = {
        'total_revenue': total_revenue,
        'grouped_data': grouped_data,
        'groups': groups,
        'selected_group': selected_group
    }

    return render(request, 'payment/revenue.html', context)


