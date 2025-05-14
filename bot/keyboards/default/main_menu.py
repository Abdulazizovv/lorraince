from aiogram.types import ReplyKeyboardMarkup,KeyboardButton


def main_menu(is_admin: bool = False) -> ReplyKeyboardMarkup:
    """
    Function to create a main menu keyboard.
    :param is_admin: Boolean value to check if the user is admin or not.
    :return: ReplyKeyboardMarkup object with the main menu buttons.
    """
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton("Soft Slide 🚪"),
            ],
            [
                KeyboardButton("Ma'lumotlarni yangilash🔄")
            ] if is_admin else [],
            [
                KeyboardButton("Yordam❓")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


    return markup