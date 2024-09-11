from datetime import date
from django.http import HttpResponse
from dateutil.relativedelta import relativedelta

from payment.models import PaymentSchedule
from student.models import Student


def dataView(request, student_id):
    # Parametrlarni butun sonlarga o'tkazamiz
    student_id = int(student_id)

    # Talaba ma'lumotlarini olish
    student = Student.objects.get(id=student_id)
    start_date = student.start_date
    current_date = date.today()

    # Talabaning to'lov qilingan oyliklarni olish
    paid_months = PaymentSchedule.objects.filter(student_id=student_id).values_list('paid_months', flat=True)

    # Kirish sanasidan hozirgi oygacha bo'lgan oylarni tekshirish
    unpaid_months = []
    month = start_date.replace(day=1)  # Kirish sanasidan boshlash

    while month <= current_date:
        # Hozirgi oy uchun to'lov qilingan sanani tekshirish
        month_str = month.strftime('%Y-%m')
        
        # Hozirgi oy ichida o'zgaruvchi kundan keyin to'lov qilish kerakmi?
        payment_day = min(start_date.day, (month + relativedelta(day=31)).day)
        payment_date = month.replace(day=payment_day)
        
        # Agar to'lov qilinmagan bo'lsa, ro'yxatga qo'shish
        if payment_date <= current_date and month_str not in paid_months:
            unpaid_months.append(month_str)
        
        month += relativedelta(months=1)

    # To'lanmagan oylar ro'yxatini foydalanuvchiga qaytarish
    if unpaid_months:
        response_content = f"Unpaid months from {start_date.strftime('%Y-%m')} to {current_date.strftime('%Y-%m')}: {', '.join(unpaid_months)}"
    else:
        response_content = "All payments are up to date from the start date."

    return HttpResponse(response_content)

def unpaidPaymentsView(request):
    current_date = date.today()
    # Hozirgi oydan orqaga 12 oyni hisoblash
    start_date = current_date - relativedelta(months=12)
    
    # Barcha talabalarni olish
    students = Student.objects.all()

    # Natijani saqlash uchun bo'sh ro'yxat
    results = []

    for student in students:
        # Talabaning start_date dan boshlab to'langan oylarni olish
        paid_months = PaymentSchedule.objects.filter(student=student).values_list('paid_months', flat=True)
        
        # Talabaning start_date dan hozirgi oygacha bo'lgan oyliklarni olish
        unpaid_months = []
        month = max(student.start_date.replace(day=1), start_date)  # Start_date student start_date yoki 12 oy orqaga qaytgan sanadan boshlanadi

        while month <= current_date:
            month_str = month.strftime('%Y-%m')
            if month_str not in paid_months:
                unpaid_months.append(month_str)
            month += relativedelta(months=1)

        if unpaid_months:
            results.append({
                'student': student,
                'unpaid_months': unpaid_months,
            })

    # Natijani HTML formatida chiqaramiz
    response_content = '<h1>Unpaid Payments Report from Student Start Date for the Last 12 Months</h1>'
    for result in results:
        response_content += f'<h2>Student: {result["student"]}</h2>'
        response_content += f'<p>Unpaid months: {", ".join(result["unpaid_months"])}</p>'

    if not results:
        response_content = '<h1>All payments are up to date for the last 12 months.</h1>'

    return HttpResponse(response_content)

def unpaidAndPaidPaymentsView(request):
    current_date = date.today()
    # Hozirgi oydan orqaga 12 oyni hisoblash
    start_date = current_date - relativedelta(months=12)
    
    # Barcha talabalarni olish
    students = Student.objects.all()

    # Natijani saqlash uchun bo'sh ro'yxat
    results = []

    for student in students:
        # Talabaning start_date dan boshlab to'langan oylarni olish
        paid_months = PaymentSchedule.objects.filter(student=student).values_list('paid_months', flat=True)

        # Talabaning start_date dan hozirgi oygacha bo'lgan oyliklarni olish
        all_months = []
        month = max(student.start_date.replace(day=1), start_date)  # Start_date student start_date yoki 12 oy orqaga qaytgan sanadan boshlanadi

        while month <= current_date:
            month_str = month.strftime('%Y-%m')
            all_months.append(month_str)
            month += relativedelta(months=1)

        # To'langan va to'lanmagan oylarni ajratish
        paid_months_list = [month for month in all_months if month in paid_months]
        unpaid_months_list = [month for month in all_months if month not in paid_months]

        if paid_months_list or unpaid_months_list:
            results.append({
                'student': student,
                'paid_months': paid_months_list,
                'unpaid_months': unpaid_months_list,
            })

    # Natijani HTML formatida chiqaramiz
    response_content = '<h1>Payments Report from Student Start Date</h1>'
    for result in results:
        response_content += f'<h2>Student: {result["student"]}</h2>'
        response_content += f'<p>Paid months: {", ".join(result["paid_months"])}</p>'
        response_content += f'<p>Unpaid months: {", ".join(result["unpaid_months"])}</p>'

    if not results:
        response_content = '<h1>All payments are up to date from the start date.</h1>'

    return HttpResponse(response_content)