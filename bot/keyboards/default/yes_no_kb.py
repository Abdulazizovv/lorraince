from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
yes_button = KeyboardButton("Ha ✅")
no_button = KeyboardButton("Yo'q ❌")
back_button = KeyboardButton("🔙 Orqaga ")
kb.add(yes_button, no_button).add(back_button)