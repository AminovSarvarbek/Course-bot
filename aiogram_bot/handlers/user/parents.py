import asyncio
from aiogram import types, Bot, Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ContentType
from aiogram.fsm.context import FSMContext
from aiogram_bot.states.parents import Guardianship
from aiogram_bot.keyboards.default.user import menu_contact_users, for_parents
from aiogram_bot.loader import dp
from asgiref.sync import sync_to_async
from student.models import Student

@dp.message(F.text == 'ota-ona')
async def parent_role(message: Message, state: FSMContext):
    # Ota-ona rolini tanlash uchun telefon raqamini yuborish
    await message.answer(
        "💭 Iltimos, telefon raqamingizni yuboring",
        reply_markup=menu_contact_users
    )
    await state.set_state(Guardianship.number)

@dp.message(F.content_type == ContentType.CONTACT)
@dp.message(F.state == Guardianship.number)
async def get_contact_info(message: Message, state: FSMContext):
    try:
        # Telefon raqamini olish va foydalanuvchini yangilash
        phone_number = message.contact.phone_number

        if phone_number.startswith("+"):
            phone_number = phone_number[1:]  # Telefon raqami formatini to'g'rilash

        # Telefon raqamiga mos keladigan foydalanuvchini topish
        user_data = await sync_to_async(Student.objects.filter(phone=phone_number).first)()

        if user_data is not None:
            user_data.telegram_id = message.chat.id
            await sync_to_async(user_data.save)()
            await message.answer(
                "Xush kelibsiz, ota-ona!",
                reply_markup=for_parents
            )
        else:
            await message.answer(
                "Telefon raqamingiz ma'lumotlar bazasida topilmadi. Iltimos, ma'lumotlaringizni tekshirib ko'ring.",
                reply_markup=menu_contact_users
            )

    except Exception as e:
        # Xato yuzaga kelganda foydalanuvchiga xabar yuborish
        print(f"Error: {e}")  # Xatolik haqida ma'lumot
        await message.answer(
            "Siz ma'lumotlar bazasiga qo'shilmadingiz! Iltimos, o'qituvchiga murojaat qiling.",
            reply_markup=menu_contact_users
        )
    finally:
        await state.clear()
