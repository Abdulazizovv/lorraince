from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def castle_types_kb(castle_types: list) -> ReplyKeyboardMarkup:
    """
    Generates a keyboard for selecting castle types.
    
    Args:
        castle_types (list): List of castle types.
    
    Returns:
        ReplyKeyboardMarkup: The generated keyboard.
    """
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for castle_type in castle_types:
        kb.add(KeyboardButton(castle_type[1]))
    kb.add(KeyboardButton("🔙 Orqaga"))
    return kb