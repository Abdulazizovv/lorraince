from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def soft_slide_mirrors_kb(mirros: list) -> ReplyKeyboardMarkup:
    """
    Create a keyboard for soft slide mirrors.
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for mirror in mirros:
        button = KeyboardButton(f"{mirror}")
        keyboard.add(button)
    back_button = KeyboardButton("Orqaga 🔙")
    keyboard.add(back_button)
    return keyboard