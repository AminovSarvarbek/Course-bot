from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class DirectionCallback(CallbackData, prefix="DirectionCallback"):
    direction: str


direction_builder = InlineKeyboardBuilder()
direction_builder.button(
    text='Ai🤖',
    callback_data=DirectionCallback(
        direction="ai"
    )
)
direction_builder.button(
    text='Fullstack🌐',
    callback_data=DirectionCallback(
        direction="fullstack"
    )
)
direction_builder.button(
    text='Mobile📱',
    callback_data=DirectionCallback(
        direction="mobile"
    )
)