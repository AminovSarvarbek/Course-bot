from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async

from aiogram_bot.loader import dp
from aiogram_bot.keyboards.default.user import parent_role_keyboard, for_parents
from aiogram_bot.keyboards.default.admin import for_admin
from student.models import Student
from user.models import CustomUser

@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    try:
        # Adminni tekshirish
        admin_exists = await sync_to_async(CustomUser.objects.filter)(telegram_id=message.chat.id, is_staff=True)
        if await sync_to_async(admin_exists.exists)():
            await message.answer("Assalomu Aleykum admin", reply_markup=for_admin)
        else:
            # Studentni tekshirish
            try:
                await sync_to_async(Student.objects.get)(telegram_id=message.chat.id)
                await message.answer("Bosh menu", reply_markup=for_parents)
            except Student.DoesNotExist:
                await message.answer("Assalomu alaykum ota-ona!", reply_markup=parent_role_keyboard)
    except Exception as e:
        # Umumiy xatoliklarni qayd etish
        print(f"Xato: {e}")
