from aiogram import Bot, Dispatcher, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ContentType
from aiogram.filters import Command
from aiogram_bot.filters.admin import IsAdminFilter
from aiogram_bot.keyboards.default.admin import for_admin
from aiogram_bot.keyboards.default.user import for_parents
from aiogram_bot.loader import dp, bot

# Handler for the /cancel command to stop all states
@dp.message(Command("exit"),IsAdminFilter())
async def cancel(message: Message, state: FSMContext):
    await state.clear()  # Clear the state for the user
    await message.answer("Operatsiya bekor qilindi. (Operation canceled.)",reply_markup=for_admin)



@dp.message(Command("exit"))
async def cancel(message: Message, state: FSMContext):
    await state.clear()  # Clear the state for the user
    await message.answer("Operatsiya bekor qilindi. (Operation canceled.)",reply_markup=for_parents)