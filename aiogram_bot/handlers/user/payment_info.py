from aiogram import F
from aiogram.types import Message
from asgiref.sync import sync_to_async
from student.models import Student
from aiogram_bot.loader import dp
from aiogram_bot.keyboards.default.user import for_parents
from payment.models import Payment
from aiogram_bot.utils.month_names import month_names
from datetime import datetime

from typing import List, Tuple

def format_payment_details(paid_month: str, payment_amount: int, payment_time: str) -> str:
    return (f"• <b>{paid_month[:4]}-yilning {month_names[int(paid_month[5:])-1]} oyi ({paid_month})</b>\n"
            f"    💰 To'lov summasi: <b>{int(payment_amount):,}</b> so'm\n"
            f"    ⏰ To'lov vaqti: <b>{payment_time}</b>\n")

def format_unpaid_months(unpaid_months: List[str], monthly_amount: int) -> Tuple[str, int]:
    unpaid_months_str = '\n'.join([
        f"• {month[:4]}-yilning {month_names[int(month[5:])-1]} oyi ({month})"
        for month in unpaid_months
    ])
    total_debt = monthly_amount * len(unpaid_months)
    return unpaid_months_str, total_debt

@dp.message(F.text == "💵 To'lov tarixi")
async def payment_history(message: Message) -> None:
    try:
        student = await sync_to_async(Student.objects.get)(telegram_id=message.chat.id)
        payments = await sync_to_async(list)(Payment.objects.filter(student=student))

        if payments:
            paid_months_str = ''
            total_paid = 0
            for payment in payments:
                paid_month = payment.paid_months
                payment_amount = payment.amount
                payment_time = payment.payment_time.strftime('%Y-%m-%d %H:%M')
                paid_months_str += format_payment_details(paid_month, payment_amount, payment_time)
                total_paid += payment_amount

            response_message = f"""
<b>💵 To'lov tarixi:</b>

🧑‍🎓 <b>Farzandingiz:</b> {student.first_name} {student.last_name}

📅 <b>To'langan oylar:</b>
{paid_months_str.strip()}

💰 <b>Jami to'langan summa:</b> <b>{int(total_paid):,}</b> so'm

📅 <b>Hozirgi oy uchun to'lov:</b> <b>{int(student.amount):,}</b> so'm
            """
        else:
            response_message = f"""
<b>📉 To'lov tarixi mavjud emas!</b>\n\n

🔍 <b>Ma'lumot:</b> Farzandingiz {student.first_name} {student.last_name} hali to'lovlarni amalga oshirmagan.
            """

        await message.answer(response_message, parse_mode="HTML", reply_markup=for_parents)

    except Student.DoesNotExist:
        await message.answer("Student ma'lumotlari topilmadi. Iltimos, ma'lumotlaringizni tekshiring.")
