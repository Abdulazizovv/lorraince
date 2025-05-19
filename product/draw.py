from PIL import Image, ImageDraw, ImageFont
from typing import Optional
import math
from product.models import SoftSlide




# DPI ko'rsatkich
DPI = 100  # yoki 72 / 96, istalgan rasm sifati uchun

def draw_softslide(door: SoftSlide, save_path: Optional[str] = "softslide_output.png"):
    """
    Har qanday SoftSlide obyektiga asoslanib eshik chizmasini yaratadi.
    """
    width_mm = door.width
    height_mm = door.height

    # Convert to pixels
    width_px = int(width_mm / 1000 * DPI * 3)  # 3x zoom
    height_px = int(height_mm / 1000 * DPI * 3)

    img = Image.new("RGB", (width_px + 100, height_px + 100), "white")
    draw = ImageDraw.Draw(img)

    offset_x, offset_y = 50, 50  # padding

    # ➤ Eshik tashqi konturi
    draw.rectangle(
        [offset_x, offset_y, offset_x + width_px, offset_y + height_px],
        outline="black",
        width=4
    )

    # ➤ Cols (ustunlar)
    col_width = width_px / door.cols
    for i in range(1, door.cols):
        x = offset_x + int(col_width * i)
        draw.line([(x, offset_y), (x, offset_y + height_px)], fill="gray", width=2)

    # ➤ Plaid (panjara) bo‘lsa
    if door.plaid:
        if door.plaid_type in [1, 3]:  # Horizontal chiziqlar
            for y in range(offset_y + 50, offset_y + height_px, 100):
                draw.line([(offset_x, y), (offset_x + width_px, y)], fill="blue", width=1)

        if door.plaid_type in [2, 3]:  # Vertical chiziqlar
            for x in range(offset_x + 50, offset_x + width_px, 100):
                draw.line([(x, offset_y), (x, offset_y + height_px)], fill="blue", width=1)

    # ➤ Castle (qulf dizayni)
    if door.castle:
        if door.castle_pos == 1:  # O‘rtada
            center_x = offset_x + width_px // 2
            draw.line([(center_x, offset_y), (center_x, offset_y + height_px)], fill="red", width=3)

        elif door.castle_pos == 2:  # Ikki chetda
            draw.line([(offset_x + 10, offset_y), (offset_x + 10, offset_y + height_px)], fill="red", width=3)
            draw.line([(offset_x + width_px - 10, offset_y), (offset_x + width_px - 10, offset_y + height_px)], fill="red", width=3)

        if door.castle_sides:
            draw.rectangle([(offset_x + 10, offset_y + 10), (offset_x + 30, offset_y + 30)], fill="red")
            draw.rectangle([(offset_x + width_px - 30, offset_y + height_px - 30), (offset_x + width_px - 10, offset_y + height_px - 10)], fill="red")

    # ➤ Taglavha (nom, o'lcham, narx)
    font = None
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except:
        font = ImageFont.load_default()

    info_text = f"W: {door.width}mm | H: {door.height}mm | Cols: {door.cols} | Price: {door.price} so'm"
    draw.text((offset_x, offset_y + height_px + 10), info_text, fill="black", font=font)

    # Save
    img.save(save_path)
    print(f"Diagram saved to: {save_path}")
