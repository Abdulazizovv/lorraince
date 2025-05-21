from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.loader import dp, db
from bot.keyboards.default.softslide_mirrors import soft_slide_mirrors_kb
from bot.keyboards.default import back_kb
from bot.keyboards.default.main_menu import main_menu
from bot.keyboards.default.yes_no_kb import kb
from bot.keyboards.default.plaid_types import plaid_types_kb
from bot.keyboards.default.castle_types import castle_types_kb
from bot.keyboards.default.select_color import select_color_kb
from bot.keyboards.default.order_again import order_again_kb
from product.models import SoftSlide, SoftSlideDye, SoftSlideElement
from product.utils import SoftSlideCalculator, SoftSlideDrawer
from product.draw import draw_softslide


@dp.message_handler(text="Soft Slide 🚪", state="*")
async def soft_slide(message: types.Message, state: FSMContext):

    await state.finish()

    # bu yerda asosiy protsess bo'ladi
    await message.answer("Balandligini kiriting(mm):", reply_markup=back_kb)
    await state.set_state("height")


@dp.message_handler(state="height")
async def get_height(message: types.Message, state: FSMContext):

    user = await db.get_or_create_user(message.from_user.id)

    if message.text == "🔙 Orqaga":
        await message.answer("Bosh sahifaga qaytdingiz.", reply_markup=main_menu(user['is_admin']))
        await state.finish()
        return


    try:
        height = int(message.text)
        if height < 0:
            await message.answer("Iltimos, balandlikni to'g'ri kiriting (mm):", reply_markup=back_kb)
            return
    except ValueError:
        await message.answer("Iltimos, balandlikni to'g'ri kiriting (mm):", reply_markup=back_kb)
        return

    await state.update_data(height=height)

    # Keyingi qadamga o'tish
    await message.answer("Enini kiriting(mm):", reply_markup=back_kb)
    await state.set_state("width")

@dp.message_handler(state="width")
async def get_width(message: types.Message, state: FSMContext):

    if message.text == "🔙 Orqaga":
        await message.answer("Balandligini kiriting(mm):", reply_markup=back_kb)
        await state.set_state("height")
        return

    try:
        width = int(message.text)
        if width < 0:
            await message.answer("Iltimos, enini to'g'ri kiriting (mm):", reply_markup=back_kb)
            return
    except ValueError:
        await message.answer("Iltimos, enini to'g'ri kiriting (mm):", reply_markup=back_kb)
        return

    await state.update_data(width=width)

    # Keyingi qadamga o'tish
    await message.answer("Razdeller sonini kiriting:", reply_markup=back_kb)
    await state.set_state("columns")

@dp.message_handler(state="columns")
async def get_columns(message: types.Message, state: FSMContext):

    if message.text == "🔙 Orqaga":
        await message.answer("Enini kiriting(mm):", reply_markup=back_kb)
        await state.set_state("width")
        return

    try:
        columns = int(message.text)
        if columns < 0:
            await message.answer("Iltimos, razdeller sonini to'g'ri kiriting:", reply_markup=back_kb)
            return
    except ValueError:
        await message.answer("Iltimos, razdeller sonini to'g'ri kiriting:", reply_markup=back_kb)
        return

    await state.update_data(columns=columns)

    user = await db.get_or_create_user(message.from_user.id)

    # Keyingi qadamga o'tish
    mirrors = await db.get_softslide_mirrors_name()
    if not mirrors:
        await message.answer("Ma'lumotlar bazasida hech qanday ma'lumot topilmadi.", reply_markup=main_menu(user['is_admin']))
        return
    
    await message.answer("Oyna turini tanlang:", reply_markup=soft_slide_mirrors_kb(mirrors))
    await state.set_state("mirror_type")


@dp.message_handler(state="mirror_type")
async def get_mirror_type(message: types.Message, state: FSMContext):

    user = await db.get_or_create_user(message.from_user.id)

    if message.text == "🔙 Orqaga":
        await message.answer("Razdellar sonini kiriting:", reply_markup=back_kb)
        await state.set_state("columns")
        return

    mirror_type = message.text

    mirror = await db.get_softslide_mirror_by_name(mirror_type)
    if not mirror:
        await message.answer("Ma'lumotlar bazasida hech qanday ma'lumot topilmadi.")
        return
    
    await state.update_data(mirror=mirror)

    await message.answer("Shatlanka kerakmi?", reply_markup=kb)
    await state.set_state("plaid")

@dp.message_handler(state="plaid")
async def get_plaid(message: types.Message, state: FSMContext):

    if message.text == "🔙 Orqaga":
        mirrors = await db.get_softslide_mirrors_name()
        await message.answer("Oyna turini tanlang:", reply_markup=soft_slide_mirrors_kb(mirrors))
        await state.set_state("mirror_type")
        return

    if message.text == "Ha ✅":
        plaid = True
        plaid_types = SoftSlide.get_plaid_types()
        await message.answer("Shatlanka qanaqasiga qo'yilsin?", reply_markup=plaid_types_kb(plaid_types))
        await state.update_data(plaid=plaid)
        await state.set_state("plaid_type")
        return
    elif message.text == "Yo'q ❌":
        plaid = False
        await state.update_data(plaid=plaid)
        await message.answer("Zamok qo'yiladimi?", reply_markup=kb)
        await state.set_state("castle")
        return
    else:
        await message.answer("Iltimos, javobni tanlang:", reply_markup=kb)
        return


@dp.message_handler(state="plaid_type")
async def get_plaid_type(message: types.Message, state: FSMContext):

    if message.text == "🔙 Orqaga":
        await message.answer("Shatlanka kerakmi?", reply_markup=kb)
        await state.set_state("plaid")
        return

    plaid_type = SoftSlide.get_plaid_type_from_name(message.text)
    await state.update_data(plaid_type=plaid_type)

    # Keyingi qadamga o'tish
    await message.answer("Zamok qo'yiladimi?", reply_markup=kb)
    await state.set_state("castle")
    return

@dp.message_handler(state="castle")
async def get_castle(message: types.Message, state: FSMContext):

    if message.text == "🔙 Orqaga":
        await message.answer("Shatlanka qo'yiladimi?", reply_markup=kb)
        await state.set_state("plaid")
        return
    
    if message.text == "Ha ✅":
        castle = True
        await state.update_data(castle=castle)
        castle_types = SoftSlide.get_castle_pos()

        await message.answer("Zamok turi:", reply_markup=castle_types_kb(castle_types))
        await state.set_state("castle_type")
        return
    
    elif message.text == "Yo'q ❌":
        castle = False
        await state.update_data(castle=castle)

        colors = SoftSlideDye.objects.values_list("name")

        await message.answer(
            "Rangni tanlang.",
            reply_markup=select_color_kb(colors)
        )

        await state.set_state("color")
        return
    else:
        await message.answer("Iltimos, javobni tanlang:", reply_markup=kb)
        return
    

@dp.message_handler(state="castle_type")
async def get_castle_type(message: types.Message, state: FSMContext):

    if message.text == "🔙 Orqaga":
        await message.answer("Zamok qo'yiladimi?", reply_markup=kb)
        await state.set_state("castle")
        return

    castle_type = SoftSlide.get_castle_pos_from_name(message.text)
    await state.update_data(castle_type=castle_type)

    # Keyingi qadamga o'tish
    colors = SoftSlideDye.objects.values_list("name")

    await message.answer(
        "Rangni tanlang.",
        reply_markup=select_color_kb(colors)
    )

    await state.set_state("color")

@dp.message_handler(state="color")
async def get_color(message: types.Message, state: FSMContext):

    user = await db.get_or_create_user(message.from_user.id)


    if message.text == "🔙 Orqaga":
        await message.answer("Zamok qo'yiladimi?", reply_markup=kb)
        await state.set_state("castle")
        return
    
    color = SoftSlideDye.objects.filter(name=message.text).first()
    if not color:
        colors = SoftSlideDye.objects.values_list("name")
        await message.answer("Tanlangan rang topilmadi. Qaytadan tanlang.", reply_markup=select_color_kb(colors))
        await state.set_state("color")
        return
    
    await state.update_data(color=color)
    data = await state.get_data()
    height = data.get("height")
    width = data.get("width")
    columns = data.get("columns")
    mirror = data.get("mirror")
    plaid = data.get("plaid")
    plaid_type = data.get("plaid_type")
    castle = data.get("castle")
    castle_type = data.get("castle_type", 1)
    color = data.get("color")

    # Yangi eshik yaratish
    soft_slide = SoftSlide(
        height=height,
        width=width,
        cols=columns,
        mirror=mirror,
        plaid=plaid,
        plaid_type=plaid_type,
        castle=castle,
        castle_pos=castle_type,
        dye=color
    )
    soft_slide.save()

    await state.update_data(door=soft_slide)


    # Hisoblash
    elements = SoftSlideElement.objects.all()

    

    soft_slide.calc_price()

    doors = data.get("doors", [])
    doors.append(soft_slide)
    await state.update_data(doors=doors)

    calculator = SoftSlideCalculator(elements, doors)
    price = calculator.calculate_total()
    print(price)
    await message.answer(
        "<i>Iltimos, kuting ...⏳</i>\n" \
        "<i>Rasm generatsiya qilinmoqda.</i>",
        parse_mode="HTML",
        reply_markup=types.ReplyKeyboardRemove()
    )
    # image = draw_softslide(soft_slide)
    image = SoftSlideDrawer().create(soft_slide)
    commissions = 0

    # if user['user_type'] == "customer":
    #     commissions += soft_slide.price + (soft_slide.price / 100) * 11.5

    await message.answer_photo(
        photo=image,
        caption=(
            f"Umumiy narx: {price + commissions} so'm\n"
        )
    )

    await message.answer("Yana buyurtma qilasizmi?", reply_markup=order_again_kb())
    await state.set_state("order_again")


@dp.message_handler(text="Xuddi shunday buyurtma berish 🔄", state="order_again")
async def order_again(message: types.Message, state: FSMContext):
    user = await db.get_or_create_user(message.from_user.id)
    data = await state.get_data()
    door = data.get("door")
    if not door:
        await message.answer("Buyurtma berish jarayonida xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.", reply_markup=main_menu(user['is_admin']))
        return
    
    await message.answer("Xuddi shunday eshikdan nechta buyurtma berasiz?", reply_markup=back_kb)
    await state.set_state("order_again_count")

@dp.message_handler(state="order_again_count")
async def get_order_again_count(message: types.Message, state: FSMContext):
    user = await db.get_or_create_user(message.from_user.id)
    if message.text == "🔙 Orqaga":
        await message.answer("Yana buyurtma qilasizmi?", reply_markup=order_again_kb())
        return

    try:
        count = int(message.text)
        if count < 0:
            await message.answer("Iltimos, buyurtma sonini to'g'ri kiriting:", reply_markup=back_kb)
            return
    except ValueError:
        await message.answer("Iltimos, buyurtma sonini to'g'ri kiriting:", reply_markup=back_kb)
        return

    data = await state.get_data()
    door = data.get("door")
    if not door:
        await message.answer("Buyurtma berish jarayonida xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.", reply_markup=main_menu(user['is_admin']))
        return
    
    # Hisoblash
    elements = SoftSlideElement.objects.all()

    calculator = SoftSlideCalculator(elements, [door] * count)
    price = calculator.calculate_total()
    print(price)

    commissions = 0

    # if user['user_type'] == "customer":
    #     commissions += door.price + (door.price / 100) * 11.5

    await message.answer(
        (
            f"Buyurtma soni: {count}\n"
            f"Umumiy narx: {price + commissions} so'm\n"
        )
    )

    await message.answer("Yana buyurtma qilasizmi?", reply_markup=order_again_kb())
    await state.set_state("order_again")


@dp.message_handler(text="O'zgartirish bilan buyurtma berish ✏️", state="order_again")
async def change_order(message: types.Message, state: FSMContext):
    user = await db.get_or_create_user(message.from_user.id)
    await message.answer("Balandligini kiriting(mm):", reply_markup=back_kb)
    await state.set_state("height")
    await state.update_data(door=None)
    return

@dp.message_handler(text="Bosh sahifaga qaytish 🔙", state="order_again")
async def back_to_main_menu(message: types.Message, state: FSMContext):
    await state.finish()
    user = await db.get_or_create_user(message.from_user.id)
    await message.answer("Bosh sahifaga qaytdingiz.", reply_markup=main_menu(user['is_admin']))
    return