from aiogram import types
from django.db.models import Value, Model
from product.models import SoftSlideElement, SoftSlideMirror, SoftSlideDye
from bot.loader import dp, db
from io import BytesIO
from pandas import DataFrame, ExcelWriter, ExcelFile, read_excel
from aiogram.dispatcher import FSMContext
import pandas as pd


@dp.message_handler(text="Ma'lumotlarni yangilash🔄", state="*")
async def update_data(message: types.Message, state: FSMContext):
    await state.finish()

    user = await db.get_or_create_user(message.from_user.id)

    if not user['is_admin']:
        return

    await message.answer("⏳ Ma'lumotlarni tayyorlanmoqda...")

    models: dict[str, Model] = {
        "soft_slide_mirrors": SoftSlideMirror,
        "soft_slide_elements": SoftSlideElement,
        "soft_slide_colors": SoftSlideDye,
    }

    c = BytesIO()
    excel = ExcelWriter(c)

    for k, v in models.items():
        df = DataFrame(
            [
                data
                async for data in v.objects.all()
                .annotate(delete=Value(""))
                .values("id", "name", "price", "unit", "formula", "delete")
            ]
        )

        df.rename(
            columns={
                "id": "ID",
                "name": "NAME",
                "price": "PRICE",
                "unit": "UNIT",
                "formula": "FORMULA",
                "delete": "DELETE",
            }
        )

        if "id" not in df:
            df["id"] = ""

        if "name" not in df:
            df["name"] = ""

        if "price" not in df:
            df["price"] = ""
        if "unit" not in df:
            df["unit"] = ""

        if "formula" not in df:
            df["formula"] = ""

        if "delete" not in df:
            df["delete"] = ""

        df.to_excel(excel, sheet_name=k, index=False)

    excel.close()

    c.seek(0)

    caption_text = (
        "Fayldagi ma'lumotlarni o'zgartirishda ID ustunini o'zgartirmang.\n"
        "Yangi ma'lumot qo'shish uchun ID ustunini bo'sh qoldiring.\n"
        "Ma'lumotlarni o'chirish uchun DELETE ustunini 1 ga o'zgartiring.\n"
    )
    await message.answer_document(
        types.InputFile(c, filename="data.xlsx"),
        caption=caption_text,
    )

    await state.set_state("get_data")

@dp.message_handler(state="get_data", content_types=types.ContentTypes.DOCUMENT)
async def get_data(message: types.Message, state: FSMContext):
    
    user = await db.get_or_create_user(message.from_user.id)
    
    if not user['is_admin']:
        await message.answer("Вы не администратор")
        return
    
    file = await message.document.get_file()
    buffer = BytesIO()
    await file.download(buffer)
    buffer.seek(0)
    shn: dict[str, type] = {
        "soft_slide_elements": SoftSlideElement,
        "soft_slide_mirrors": SoftSlideMirror,
        "soft_slide_colors": SoftSlideDye,
    }

    excel = ExcelFile(buffer)

    added = deleted = updated = 0

    for sheet, model in shn.items():
        try:
            df = read_excel(excel, sheet_name=sheet)
        except ValueError:
            continue  # Sheet not found

        for id, name, price, unit, formula, delete in df.values:
            name = str(name).strip() if pd.notna(name) else ""

            if delete == 1:
                model.objects.filter(id=id).delete()
                deleted += 1
            elif pd.isna(id):
                model.objects.create(name=name, price=price, formula=formula, unit=unit)
                added += 1
            else:
                model.objects.filter(id=id).update(name=name, price=price, formula=formula)
                updated += 1

    await message.answer(
        f"Ma'lumotlar yuklandi.\n\n"
        f"{added} ta ma'lumot qo'shildi.\n"
        f"{updated} ta ma'lumot yangilandi.\n"
        f"{deleted} ta ma'lumot o'chirildi."
    )
    await state.finish()