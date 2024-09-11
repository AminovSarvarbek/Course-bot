from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Create contact request keyboard
menu_contact_users = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text='📞 Send phone number',
                request_contact=True  # This requests the user's contact information
            )
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Create parent role selection keyboard
parent_role_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="ota-ona"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Create options for parents (child info and payment history)
for_parents = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Farzandimning malumotlari📕"),
        ],
        [
            KeyboardButton(text="💵 To'lov tarixi"),
            KeyboardButton(text="📉 Qarzdorlik"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


