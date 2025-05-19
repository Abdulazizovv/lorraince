from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def select_color_kb(colors: list):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for color in colors:
        kb.add(KeyboardButton(color[0]))
    kb.add(KeyboardButton("🔙 Orqaga"))
    return kb