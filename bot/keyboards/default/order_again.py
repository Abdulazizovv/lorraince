from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def order_again_kb():
    """
    Keyboard for the order again button
    :return: ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton("Xuddi shunday buyurtma berish 🔄")
    button2 = KeyboardButton("O'zgartirish bilan buyurtma berish ✏️")
    button3 = KeyboardButton("Bosh sahifaga qaytish 🔙")
    keyboard.add(button)
    keyboard.add(button2)
    keyboard.add(button3)
    return keyboard