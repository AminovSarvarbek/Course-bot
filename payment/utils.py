from datetime import date
from dateutil.relativedelta import relativedelta
from asgiref.sync import sync_to_async
from student.models import Student
from payment.models import Payment

def get_students_with_unpaid_months(group_name=None):
    """
    Retrieve a list of students along with the months they have not paid for,
    based on their start date and optional group name filter.
    """
    current_date = date.today()  # Get today's date
    results = []

    # Fetch all students, optionally filter by group name
    students = Student.objects.filter(group__name=group_name) if group_name else Student.objects.all()

    for student in students:
        # Fetch the list of paid months for the student
        paid_months = Payment.objects.filter(student=student).values_list('paid_months', flat=True)
        
        # Initialize the list of unpaid months
        unpaid_months = []

        # Start checking from the student's start date
        month = student.start_date.replace(day=1)

        # Check each month from the start date to the current date
        while month <= current_date.replace(day=1):
            month_str = month.strftime('%Y-%m')  # Convert month to YYYY-MM format

            # Skip the current month if it matches the start month
            if month == student.start_date.replace(day=1) and month == current_date.replace(day=1):
                break

            # If the month is unpaid, add it to the list
            if month_str not in paid_months:
                unpaid_months.append(month_str)

            # Move to the next month
            month += relativedelta(months=1)
        
        # If there are unpaid months, add the result
        if unpaid_months:
            results.append({
                'student': student,
                'unpaid_months': unpaid_months,
            })

    return results

async def get_unpaid_months_for_student(student_id):
    """
    Asynchronously retrieve the list of months a student has not paid for, based on their start date and the current date.
    """
    # Fetch the student and their start date asynchronously
    student = await sync_to_async(Student.objects.get)(id=student_id)
    start_date = student.start_date
    current_date = date.today()

    # Asynchronously fetch the paid months for the student
    paid_months = await sync_to_async(
        lambda: list(Payment.objects.filter(student_id=student_id).values_list('paid_months', flat=True))
    )()

    # List to store the months the student has not paid for
    unpaid_months = []
    month = start_date.replace(day=1)

    while month <= current_date:
        month_str = month.strftime('%Y-%m')
        payment_day = min(start_date.day, (month + relativedelta(day=31)).day)
        payment_date = month.replace(day=payment_day)

        if payment_date <= current_date and month_str not in paid_months:
            unpaid_months.append(month_str)
        
        month += relativedelta(months=1)

    return unpaid_months


async def get_paid_months_for_student(student_id):
    """
    Asynchronously retrieve the list of months a student has paid for, based on their start date and the current date.
    """
    # Fetch the student and their start date asynchronously
    student = await sync_to_async(Student.objects.get)(id=student_id)
    start_date = student.start_date
    current_date = date.today()

    # Asynchronously fetch the paid months for the student
    paid_months = await sync_to_async(
        lambda: list(Payment.objects.filter(student_id=student_id).values_list('paid_months', flat=True))
    )()

    # List to store the months the student has paid for
    paid_months_list = []

    # Check each month from the start date to the current date
    month = start_date.replace(day=1)

    while month <= current_date:
        month_str = month.strftime('%Y-%m')
        payment_day = min(start_date.day, (month + relativedelta(day=31)).day)
        payment_date = month.replace(day=payment_day)

        if payment_date <= current_date and month_str in paid_months:
            paid_months_list.append(month_str)
        
        month += relativedelta(months=1)

    return paid_months_list


