from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from asgiref.sync import sync_to_async
from user.models import CustomUser
from aiogram_bot.states.admin import AdState
from aiogram_bot.filters.admin import IsAdminFilter
from student.models import Student
import logging

from aiogram_bot.loader import dp, bot


class AdState(StatesGroup):
    content = State()  # Hold the state for receiving ad content


@dp.message(F.text == "✉️ Send Message", IsAdminFilter())
async def start_advertisement(message: Message, state: FSMContext):
    """
    Admin tomonidan xabar yuborishni boshlash uchun qo'ng'iroq qilinadi.
    """
    await message.answer("📢 Reklamani yuborishingiz mumkin: bu rasm, video yoki matnli xabar bo'lishi mumkin. Iltimos, xabarni yuboring.")
    await state.set_state(AdState.content)


@dp.message(AdState.content)
async def receive_advertisement_content(message: Message, state: FSMContext):
    """
    Reklamani qabul qilib, barcha foydalanuvchilarga tarqatadi.
    """
    users_with_telegram_id = await sync_to_async(list)(
        Student.objects.filter(telegram_id__isnull=False).values_list('telegram_id', flat=True)
    )
    
    if message.photo:
        media_type = "photo"
        file_id = message.photo[-1].file_id  # Eng yuqori sifatli rasm
        caption = message.caption or ""
    elif message.video:
        media_type = "video"
        file_id = message.video.file_id
        caption = message.caption or ""
    else:
        media_type = "text"
        text_message = message.text

    # Reklamani barcha foydalanuvchilarga yuborish
    for user_id in users_with_telegram_id:
        try:
            if media_type == "photo":
                await bot.send_photo(chat_id=user_id, photo=file_id, caption=caption)
            elif media_type == "video":
                await bot.send_video(chat_id=user_id, video=file_id, caption=caption)
            else:
                await bot.send_message(chat_id=user_id, text=text_message)
        except Exception as e:
            logging.error(f"{user_id} ga reklamani yuborishda xatolik yuz berdi: {e}")

    await message.answer("🎉 Reklama barcha foydalanuvchilarga muvaffaqiyatli yuborildi!")
    await state.clear()
