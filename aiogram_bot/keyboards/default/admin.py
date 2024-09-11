from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Create contact request keyboard with two buttons
for_admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📁 Upload Excel'),KeyboardButton(text='✉️ Send Message'),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
