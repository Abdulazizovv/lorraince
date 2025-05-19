from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def plaid_types_kb(plaid_types: list) -> ReplyKeyboardMarkup:
    """
    Create a keyboard for plaid types.
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for plaid_type in plaid_types:
        button = KeyboardButton(f"{plaid_type[1]}")
        keyboard.add(button)
    back_button = KeyboardButton("🔙 Orqaga ")
    keyboard.add(back_button)
    return keyboard