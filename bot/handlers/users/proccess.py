from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.loader import dp, db


@dp.message_handler(text="Soft Slide 🚪", state="*")
async def soft_slide(message: types.Message, state: FSMContext):

    await state.finish()

    # bu yerda asosiy protsess bo'ladi
    