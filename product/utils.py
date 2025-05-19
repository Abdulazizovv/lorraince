from io import BytesIO
import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from product.models import SoftSlide, SoftSlideElement


def toImgOpenCV(imgPIL) -> np.ndarray:
    i = np.array(imgPIL)
    red = i[:, :, 0].copy()
    i[:, :, 0] = i[:, :, 2].copy()
    i[:, :, 2] = red
    return i


def add_transparent_image(
    background: np.ndarray, foreground: np.ndarray, x_offset=None, y_offset=None
):
    bg_h, bg_w, bg_channels = background.shape
    fg_h, fg_w, fg_channels = foreground.shape

    assert (
        bg_channels == 3
    ), f"background image should have exactly 3 channels (RGB). found:{bg_channels}"
    assert (
        fg_channels == 4
    ), f"foreground image should have exactly 4 channels (RGBA). found:{fg_channels}"

    # center by default
    if x_offset is None:
        x_offset = (bg_w - fg_w) // 2
    if y_offset is None:
        y_offset = (bg_h - fg_h) // 2

    w = min(fg_w, bg_w, fg_w + x_offset, bg_w - x_offset)
    h = min(fg_h, bg_h, fg_h + y_offset, bg_h - y_offset)

    if w < 1 or h < 1:
        return

    # clip foreground and background images to the overlapping regions
    bg_x = max(0, x_offset)
    bg_y = max(0, y_offset)
    fg_x = max(0, x_offset * -1)
    fg_y = max(0, y_offset * -1)
    foreground = foreground[fg_y : fg_y + h, fg_x : fg_x + w]
    background_subsection = background[bg_y : bg_y + h, bg_x : bg_x + w]

    # separate alpha and color channels from the foreground image
    foreground_colors = foreground[:, :, :3]
    alpha_channel = foreground[:, :, 3] / 255  # 0-255 => 0.0-1.0

    # construct an alpha_mask that matches the image shape
    alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))

    # combine the background with the overlay image weighted by alpha
    composite = (
        background_subsection * (1 - alpha_mask) + foreground_colors * alpha_mask
    )

    # overwrite the section of the background image that has been updated
    background[bg_y : bg_y + h, bg_x : bg_x + w] = composite


def carry(dw, ms=6, mnc=1.5):
    a = dw // ms
    b = (a + 1) * ms
    c = b - dw
    return b if c <= mnc else dw


class SoftSlideDrawer:
    # maxwidth, maxheight = 3242, 1805
    maxwidth, maxheight = 2999, 1606
    padding = 500

    def __init__(self):
        self.fonts = {
            n: ImageFont.truetype("src/Inter.ttf", size=n) for n in range(20, 100)
        }
        self.cross = cv2.imread("src/cross.png", cv2.IMREAD_UNCHANGED)
        self.logo = cv2.imread("src/logo.png")

    def draw_text(self, draw, x, y, text, color, fontSize):
        # img = Image.new("RGB", (3309, 2339))
        # draw = ImageDraw.Draw(img)
        draw.text(
            (x, y),
            text,
            color,
            self.fonts[fontSize // 1],
        )

    def res_resize(self, img2) -> np.ndarray:
        f1 = self.maxwidth / img2.shape[1]
        f2 = self.maxheight / img2.shape[0]
        f = min(f1, f2)  # resizing factor
        dim = (int(img2.shape[1] * f), int(img2.shape[0] * f))
        r = cv2.resize(img2, dim)
        return r

    def draw_rect(self, img, x1, y1, width, height, color, borderColor, thickness):
        cv2.rectangle(img, (x1, y1), (x1 + width, y1 + height), color, -1)
        if thickness != -1:
            cv2.rectangle(
                img, (x1, y1), (x1 + width, y1 + height), borderColor, thickness
            )

    def add_image(self, x, y, img1, img2):
        img1[y : y + img2.shape[0], x : x + img2.shape[1]] = img2

    def arrow(self, img, pt1, pt2, color, thickness, tipLenth=0.06):
        cv2.arrowedLine(
            img, pt1, pt2, color, thickness, cv2.LINE_AA, tipLength=tipLenth
        )
        cv2.arrowedLine(
            img, pt2, pt1, color, thickness, cv2.LINE_AA, tipLength=tipLenth
        )

    def text_with_color(
        self, d, x, y, fontSize, texts: list[str], colors: tuple[int, int, int]
    ):
        # d = ImageDraw.ImageDraw(Image.open("aa.jpg"))
        lx = 0
        for t, c in zip(texts, colors):
            (left, top, right, bottom) = self.fonts[fontSize].getbbox(f"{t} ")
            w = right - left
            h = bottom - top
            self.draw_text(d, x + lx, y, t, (c), (fontSize))
            lx += w

    def create(self, door: "SoftSlide"):
        img_pil = Image.new("RGB", (3309, 2339), 0xFFFFFF)
        d = ImageDraw.Draw(img_pil)

        self.text_with_color(
            d,
            71,
            81,
            50,
            ["профилъ: ", "турецкий алюминиевый профиль "],
            [(255, 0, 0), (0, 0, 0)],
        )
        self.text_with_color(
            d,
            71,
            152,
            50,
            [f"стекло: ", f"стеклопакет 4х4  {door.mirror.name}"],
            [(255, 0, 0), (0, 0, 0)],
        )
        self.text_with_color(
            d,
            71,
            223,
            50,
            [f"способ открывания: ", "раздвижная "],
            [(255, 0, 0), (0, 0, 0)],
        )
        self.text_with_color(
            d,
            71,
            294,
            50,
            ["доводчики: ", "нет"],
            [(255, 0, 0), (0, 0, 0)],
        )
        self.text_with_color(
            d,
            71,
            365,
            50,
            ["объем: ", "{:.2f}m2".format((door.width / 1000) * (door.height / 1000))],
            [(255, 0, 0), (0, 0, 0)],
        )

        self.text_with_color(
            d,
            71,
            436,
            50,
            ["система: ", " Soft Slide"],
            [(255, 0, 0), (0, 0, 0)],
        )

        img = toImgOpenCV(img_pil)
        img_pil.close()

        rect = self.generate(door)

        r = self.res_resize(rect)

        y = ((img.shape[0] - r.shape[0]) // 2) + 200
        x = (img.shape[1] - r.shape[1]) // 2

        img[y : y + r.shape[0], x : x + r.shape[1]] = r

        rows, cols, channels = self.logo.shape

        img[0:rows, img.shape[1] - cols : img.shape[1]] = self.logo

        success, buffer = cv2.imencode(".png", img)
        return BytesIO(buffer)
        # cv2.imencode("res.png", img)

    def generate(self, door: "SoftSlide"):
        rect = np.zeros((door.height + 700, door.width + 700, 3))
        rect.fill(255)


        self.draw_rect(
            rect,
            self.padding,
            self.padding,
            door.width,
            door.height,
            (255, 255, 255),
            (255, 0, 0),
            5,
        )

        self.draw_sizes(door, rect)
        # self.draw_plaid(door, rect)



        self.draw_rect(
            rect,
            self.padding,
            self.padding,
            door.width,
            20,
            (153, 153, 153),
            (0, 0, 0),
            3,
        )

        self.draw_rect(
            rect,
            self.padding,
            self.padding,
            20,
            door.height,
            (153, 153, 153),
            (0, 0, 0),
            3,
        )
        self.draw_rect(
            rect,
            door.width + self.padding,
            self.padding,
            -20,
            door.height,
            (153, 153, 153),
            (0, 0, 0),
            3,
        )

        if door.cols % 2 != 0 or door.castle_pos == 2:
            self.draw_rect(
                rect,
                self.padding,
                self.padding + door.height - (door.height // 2),
                40,
                (door.height // 3),
                (153, 153, 153),
                (0, 0, 0),
                5,
            )
            self.draw_rect(
                rect,
                self.padding + door.width - 50,
                self.padding + door.height - (door.height // 2),
                40,
                (door.height // 3),
                (153, 153, 153),
                (0, 0, 0),
                5,
            )
        else:
            self.draw_rect(
                rect,
                self.padding + door.width // 2,
                self.padding + door.height - (door.height // 2),
                40,
                (door.height // 3),
                (153, 153, 153),
                (0, 0, 0),
                5,
            )
            self.draw_rect(
                rect,
                self.padding + door.width // 2 - 50,
                self.padding + door.height - (door.height // 2),
                40,
                (door.height // 3),
                (153, 153, 153),
                (0, 0, 0),
                5,
            )


        s, b = cv2.imencode(".png", rect)

        f = open("res2.png", "wb")
        f.write(b)
        f.close()

        return rect
    
    def draw_sizes(self, door: "SoftSlide", rect: np.ndarray):
        tlw = 50 / door.width
        tlh = 50 / door.height

        self.arrow(
            rect,
            (self.padding, self.padding - 70),
            (door.width + self.padding, self.padding - 70),
            (255, 0, 0),
            5,
            tlw,
        )

        cv2.putText(
            rect,
            str(door.width),
            ((door.width // 2) + self.padding // 2, self.padding - 130),
            cv2.FONT_HERSHEY_SIMPLEX,
            4,
            (255, 0, 0),
            thickness=10,
        )

        self.arrow(
            rect,
            (self.padding - 70, self.padding),
            (self.padding - 70, door.height + self.padding),
            (255, 0, 0),
            5,
            tlh,
        )

        cv2.putText(
            rect,
            str(door.height),
            (0, (door.height // 2) + self.padding),
            cv2.FONT_HERSHEY_SIMPLEX,
            4,
            (255, 0, 0),
            thickness=10,
        )

        if door.cols > 1:
            w = door.width // door.cols
            for i in range(door.cols):


                tl = 50 / w
                self.arrow(
                    rect,
                    (
                        (w * i + self.padding) + (5 if (i != 0) else 0),
                        door.height + (self.padding + 70),
                    ),
                    (
                        (w * i + self.padding + w) - (5 if (i != door.cols - 1) else 0),
                        door.height + (self.padding + 70),
                    ),
                    (2550, 0, 0),
                    5,
                    tl,
                )
                ts = cv2.getTextSize(str(w), cv2.FONT_HERSHEY_SIMPLEX, 4, 5)[0]
                x = (w * i) + w - (ts[0] // 2)

                cv2.putText(
                    rect,
                    str(w),
                    (x, door.height + self.padding + 170),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    4,
                    (255, 0, 0),
                    thickness=5,
                )
                self.draw_rect(
                    rect,
                    (w * i + self.padding),
                    (self.padding + 20),
                    w,
                    door.height - 20,
                    (255, 255, 153),
                    (0, 0, 0),
                    -1,
                )
                if door.plaid and door.plaid_type == 1:
                    x1 = (w * i + self.padding) + (150)
                    y = self.padding + 50


                    x2 = (w * i + self.padding) + w - (150)
                    y2 = self.padding + 50




                    cv2.line(
                        rect,
                        (
                            x1,y2
                        ),
                        (
                            x1,
                            y2+door.height - 80
                        ),
                        (0,0,0),
                        5
                    )
                    cv2.line(
                        rect,
                        (
                            x2,y2
                        ),
                        (
                            x2 ,
                            y2+door.height - 80
                        ),
                        (0,0,0),
                        5
                    )


                    x3 = (w * i + self.padding)
                    y3 = door.height + self.padding - 800



                    cv2.line(
                        rect,
                        (
                            x3,y3
                        ),
                        (
                            x3 + w,
                            y3
                        ),
                        (0,0,0),
                        5
                    )
                    x4 = (w * i + self.padding)
                    y4 = door.height + self.padding - 950

                    cv2.line(
                        rect,
                        (
                            x4,y4
                        ),
                        (
                            x4 + w,
                            y4
                        ),
                        (0,0,0),
                        5
                    )

                if door.plaid and door.plaid_type == 3:
                    x = (w * i + self.padding) + (w//2)
                    y = self.padding + 50




                    cv2.line(
                        rect,
                        (
                            x,
                            y
                        ),
                        (
                            x,
                            y+door.height - 80
                        ),
                        (0,0,0),
                        5
                    )


                if door.plaid and door.plaid_type in [2,3]:
                    x = (w* i * self.padding)
                    y = (self.padding + 50)

                    h = door.height

                    for splits in range(3, 10):
                        split_height = h // splits

                        if split_height < 700:
                            print(split_height,i)
                            for j in range(splits):
                                # top_left = (x,int(y+i*split_height))
                                # bottom_right = (x + w, int(y + (i + 1) * split_height))
                                pt1 = (
                                    w*i+self.padding,
                                    self.padding + (split_height * j)
                                )
                                pt2 = (
                                    w*i+self.padding + w,
                                    int(self.padding + (split_height * j))
                                )
                                print(pt1,pt2)
                                cv2.line(
                                    rect,
                                    pt1,
                                    pt2,
                                    (0,0,0),
                                    5
                                )
                            break

                if door.castle_pos == 2:
                    self.arrow(
                        rect,
                        (
                            (w * i + self.padding) + w // 4,
                            self.padding + (door.height // 2),
                        ),
                        (
                            (w * i + self.padding) + ((w // 4) * 3),
                            self.padding + (door.height // 2),
                        ),
                        (0, 0, 255),
                        15,
                        tipLenth=100 / (w / 4 * 3),
                    )
                else:
                    if i != 0 and i != door.cols - 1:
                        self.arrow(
                            rect,
                            (
                                (w * i + self.padding) + w // 4,
                                self.padding + (door.height // 2),
                            ),
                            (
                                (w * i + self.padding) + ((w // 4) * 3),
                                self.padding + (door.height // 2),
                            ),
                            (0, 0, 255),
                            15,
                            tipLenth=100 / (w / 4 * 3),
                        )
                    else:
                        add_transparent_image(
                            rect,
                            self.cross,
                            # self.handle,
                            (w * i + self.padding)
                            + (w // 2)
                            - (self.cross.shape[0] // 2),
                            self.padding
                            + (door.height // 2)
                            - ((self.cross.shape[1] // 2)),
                        )
                if i != 0:
                    cv2.rectangle(
                        rect,
                        (
                            (w * i + (self.padding - 5)),
                            door.height + self.padding + 25,
                        ),
                        (
                            (w * i + (self.padding + 5)),
                            door.height + self.padding + 115,
                        ),
                        (0, 0, 255),
                        -1,
                    )
                    self.draw_rect(
                        rect,
                        ((w * i + self.padding)),
                        (self.padding + 20),
                        20,
                        door.height - 20,
                        (153, 153, 153),
                        (0, 0, 0),
                        -1,
                    )

                if i != (door.cols - 1):
                    self.draw_rect(
                        rect,
                        ((w * i + self.padding) + w) - 20,
                        (self.padding + 20),
                        40,
                        door.height - 20,
                        (153, 153, 153),
                        (0, 0, 0),
                        -1,
                    )

                self.draw_rect(
                    rect,
                    (w * i + self.padding),
                    self.padding + 20,
                    w,
                    30,
                    (153, 153, 153),
                    (0, 0, 0),
                    3,
                )
                self.draw_rect(
                    rect,
                    (w * i + (self.padding)),
                    door.height + self.padding,
                    w,
                    -30,
                    (153, 153, 153),
                    (0, 0, 0),
                    3,
                )

        else:
            self.draw_rect(
                rect,
                (self.padding),
                self.padding + 20,
                door.width,
                door.height - 20,
                (255, 255, 153),
                (0, 0, 0),
                3,
            )
            self.draw_rect(
                rect,
                (self.padding),
                self.padding + 20,
                door.width,
                30,
                (153, 153, 153),
                (0, 0, 0),
                3,
            )

            self.draw_rect(
                rect,
                (self.padding),
                door.height + self.padding,
                door.width,
                -30,
                (153, 153, 153),
                (0, 0, 0),
                3,
            )
    

class SoftSlideCalculator:
    def __init__(self, elements: list["SoftSlideElement"], doors: list["SoftSlide"]):
        self.elements = elements  # elementlar (profil, shisha, tutqich...)
        self.doors = doors        # bir nechta eshiklar

    def calculate_total(self):
        total_cost = 0
        results = []

        for element in self.elements:
            leftover = 0
            total_units = 0
            total_price = 0

            for door in self.doors:
                need = element.calc_price(door)

                # Agar bu element uzunlikka oid bo'lsa (masalan, profil)
                if element.unit in ["m", "metr", "m."]:
                    if leftover >= need:
                        leftover -= need
                    else:
                        required = need - leftover
                        used = carry(required)  # yangi bo‘lak olinadi
                        total_units += used
                        leftover = used - required
                else:
                    total_units += need  # m² yoki dona bo‘lsa, to‘g‘ridan-to‘g‘ri qo‘shamiz

            total_price = total_units * element.price
            total_cost += total_price

            results.append({
                "element": element.name,
                "unit": element.unit,
                "total": round(total_units, 2),
                "price": round(total_price, 2),
            })

        color_glass_total = 0
        for door in self.doors:
            door_extra_price = door.dye.calc_price(door) + door.mirror.calc_price(door)
            color_glass_total += door_extra_price

            results.append({
                "element": f"Rang: {door.dye.name}, Oyna: {door.mirror.name}",
                "unit": "dona",
                "total": 1,
                "price": round(door_extra_price, 2),
            })
            total_cost += color_glass_total

        return {
            "items": results,
            "total_cost": round(total_cost, 2)
        }




