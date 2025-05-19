from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


back_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔙 Orqaga"),
        ],
    ],
    resize_keyboard=True
)