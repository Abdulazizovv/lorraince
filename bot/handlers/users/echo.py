from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.loader import dp
from product.models import SoftSlide
from product.utils import SoftSlideDrawer


@dp.message_handler(state='*', content_types=types.ContentTypes.ANY)
async def echo_all(message: types.Message, state: FSMContext):
    door = SoftSlide.objects.last()
    image = SoftSlideDrawer().create(door)
    await message.answer_photo(photo=image, caption=f"Height: {door.height} \nWidth: {door.width}")