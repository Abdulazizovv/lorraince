from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from bot.loader import dp, db
from bot.keyboards.default.main_menu import main_menu

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    
    user = await db.get_or_create_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name,
        is_bot=message.from_user.is_bot
    )

    await message.answer(
        f"Assalomu alaykum, <b>{message.from_user.full_name}</b>!\n", reply_markup=main_menu(user['is_admin'])
    )


