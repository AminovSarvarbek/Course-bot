from aiogram import F
from aiogram.types import Message
from asgiref.sync import sync_to_async
from student.models import Student
from aiogram_bot.loader import dp
from aiogram_bot.keyboards.default.user import for_parents
from payment.utils import get_unpaid_months_for_student
from aiogram_bot.utils.month_names import month_names

from typing import List, Tuple

def format_unpaid_months(unpaid_months: List[str], monthly_amount: int) -> Tuple[str, int]:
    unpaid_months_str = '\n'.join([
        f"• <b>{month[:4]}-yilning {month_names[int(month[5:])-1]} oyi ({month})</b>\n"
        f"  🗓️ To'lanmagan summa: <b>{int(monthly_amount):,}</b> so'm"
        for month in unpaid_months
    ])
    total_debt = monthly_amount * len(unpaid_months)
    return unpaid_months_str, total_debt

def generate_debt_info_message(student, unpaid_months_str: str, total_debt: int, monthly_amount: int, unpaid_months_count: int) -> str:
    if unpaid_months_str:
        return f"""
<b>📋 Qarzdorlik haqida ma'lumot:</b>

🧑‍🎓 <b>Farzandingiz:</b> {student.first_name} {student.last_name}
💵 <b>Har oy uchun to'lov:</b> <b>{int(monthly_amount):,}</b> so'm

📅 <b>To'lanmagan oylar ({unpaid_months_count} ta):</b>

{unpaid_months_str}

💰 <b>Jami qarzdorlik:</b> <b>{int(total_debt):,}</b> so'm
        """
    else:
        return f"""
<b>🎉 Qarzdorlik mavjud emas!</b>

👏 <b>Tabriklaymiz!</b> Farzandingiz {student.first_name} {student.last_name} barcha to'lovlarni to'liq amalga oshirgan.
        """

@dp.message(F.text == "📉 Qarzdorlik")
async def debt_info(message: Message) -> None:
    try:
        student = await sync_to_async(Student.objects.get)(telegram_id=message.chat.id)

        # Get unpaid months
        unpaid_months = await get_unpaid_months_for_student(student.id)

        if unpaid_months:
            monthly_amount = student.amount
            unpaid_months_str, total_debt = format_unpaid_months(unpaid_months, monthly_amount)
            unpaid_months_count = len(unpaid_months)

            response_message = generate_debt_info_message(
                student, unpaid_months_str, total_debt, monthly_amount, unpaid_months_count
            )
        else:
            response_message = generate_debt_info_message(
                student, '', 0, 0, 0
            )

        await message.answer(response_message, parse_mode="HTML", reply_markup=for_parents)

    except Student.DoesNotExist:
        await message.answer("Student ma'lumotlari topilmadi. Iltimos, ma'lumotlaringizni tekshiring.")
