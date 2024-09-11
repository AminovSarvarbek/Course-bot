from aiogram import F
from aiogram.types import Message
from asgiref.sync import sync_to_async

from aiogram_bot.loader import dp
from aiogram_bot.keyboards.default.user import for_parents
from student.models import Student


@dp.message(F.text == "Farzandimning malumotlari📕")
async def parent_info(message: Message):
    try:
        student = await sync_to_async(Student.objects.select_related('group').get)(telegram_id=message.chat.id)

        response_message = f"""
<b>👤 To'liq ism:</b> {student.first_name} {student.last_name} {student.father_name}
<b>📞 Telefon raqami:</b> +{student.phone}
<b>🏫 Maktab:</b> {student.school_name}
<b>📚 Sinfi:</b> {student.student_class}
<b>👥 Guruh nomi:</b> <b>{student.group.name}</b>
<b>💰 To'lov miqdori:</b> <b>{int(student.amount):,}</b> so'm
<b>📅 Kelgan kuni:</b> {student.start_date}
"""

        await message.answer(response_message, parse_mode="HTML",reply_markup=for_parents)

    except Student.DoesNotExist:
        pass
        print("[child_information.py]: chat id xato")

