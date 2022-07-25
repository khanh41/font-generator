import os
import random
import random as rnd

from PIL import Image, ImageColor, ImageFont, ImageDraw

r = lambda: random.randint(0, 255)


def generate(
        text,
        font,
        text_color,
        font_size,
        orientation,
        space_width,
        character_spacing,
        fit,
        word_split,
        stroke_width=0,
        stroke_fill="#282828",
        image_dir=None
):
    if orientation == 0:
        return _generate_horizontal_text(
            text,
            font,
            text_color,
            font_size,
            space_width,
            character_spacing,
            fit,
            word_split,
            stroke_width,
            stroke_fill,
            image_dir
        )
    elif orientation == 1:
        return _generate_vertical_text(
            text, font, text_color, font_size, space_width, character_spacing, fit,
            stroke_width, stroke_fill,
        )
    else:
        raise ValueError("Unknown orientation " + str(orientation))


def _generate_horizontal_text(
        text, font, text_color, font_size, space_width, character_spacing, fit, word_split,
        stroke_width=0, stroke_fill="#282828", background_path=None
):
    images = os.listdir(background_path)
    txt_img = Image.open(
        os.path.join(background_path, images[rnd.randint(0, len(images) - 1)])
    )

    txt_img_draw = ImageDraw.Draw(txt_img)

    random_y_list = []
    transcription_point_list = []
    for i, p in enumerate(text):
        fill_temp, stroke_fill_temp = ((0, 0, 0), (0, 0, 0))
        image_font = ImageFont.truetype(font=font, size=txt_img.size[1] // random.randint(20, 30))
        text_width, text_height = image_font.getsize(p)

        count_try = 0
        while True:
            if count_try >= 10:
                y1 = y2 = -1
                break

            y1 = random.randint(0, txt_img.size[1])
            y2 = y1 + text_height
            if y2 > txt_img.size[1]:
                y1 -= text_height
                y2 -= text_height

            is_ok = True
            for y1_exist, y2_exist in random_y_list:
                if not set(range(y1, y2)).isdisjoint(set(range(y1_exist, y2_exist))):
                    is_ok = False
                    count_try += 1
                    break

            if is_ok:
                random_y_list.append((y1, y2))
                break

        x1 = random.randint(0, txt_img.size[0])
        x2 = x1 + text_width
        if x2 > txt_img.size[0]:
            x1 -= text_width
            x2 -= text_width

        if x1 < 0 or x2 > txt_img.size[0] or y1 < 0 or y2 > txt_img.size[1]:
            continue

        txt_img_draw.text(
            (x1, y1),
            p,
            fill=fill_temp,
            font=image_font,
            stroke_width=stroke_width,
            stroke_fill=stroke_fill_temp,
        )

        transcription_point_list.append({"transcription": p, "points": [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]})

    return txt_img, transcription_point_list


def _generate_vertical_text(
        text, font, text_color, font_size, space_width, character_spacing, fit,
        stroke_width=0, stroke_fill="#282828"
):
    image_font = ImageFont.truetype(font=font, size=font_size)

    space_height = int(image_font.getsize(" ")[1] * space_width)

    char_heights = [
        image_font.getsize(c)[1] if c != " " else space_height for c in text
    ]
    text_width = max([image_font.getsize(c)[0] for c in text])
    text_height = sum(char_heights) + character_spacing * len(text)

    txt_img = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
    txt_mask = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))

    txt_img_draw = ImageDraw.Draw(txt_img)
    txt_mask_draw = ImageDraw.Draw(txt_mask)

    colors = [ImageColor.getrgb(c) for c in text_color.split(",")]
    c1, c2 = colors[0], colors[-1]

    fill = (
        rnd.randint(c1[0], c2[0]),
        rnd.randint(c1[1], c2[1]),
        rnd.randint(c1[2], c2[2]),
    )

    stroke_colors = [ImageColor.getrgb(c) for c in stroke_fill.split(",")]
    stroke_c1, stroke_c2 = stroke_colors[0], stroke_colors[-1]

    stroke_fill = (
        rnd.randint(stroke_c1[0], stroke_c2[0]),
        rnd.randint(stroke_c1[1], stroke_c2[1]),
        rnd.randint(stroke_c1[2], stroke_c2[2]),
    )

    for i, c in enumerate(text):
        txt_img_draw.text(
            (0, sum(char_heights[0:i]) + i * character_spacing),
            c,
            fill=fill,
            font=image_font,
            stroke_width=stroke_width,
            stroke_fill=stroke_fill,
        )
        txt_mask_draw.text(
            (0, sum(char_heights[0:i]) + i * character_spacing),
            c,
            fill=(i // (255 * 255), i // 255, i % 255),
            font=image_font,
            stroke_width=stroke_width,
            stroke_fill=stroke_fill,
        )

    if fit:
        return txt_img.crop(txt_img.getbbox()), txt_mask.crop(txt_img.getbbox())
    else:
        return txt_img, txt_mask


def random_color(text_color=None, stroke_fill=None):
    if text_color and stroke_fill:
        colors = [ImageColor.getrgb(c) for c in text_color.split(",")]
        stroke_colors = [ImageColor.getrgb(c) for c in stroke_fill.split(",")]
    else:
        colors = [(r(), r(), r()), (r(), r(), r())]
        stroke_colors = [(r(), r(), r()), (r(), r(), r())]
    c1, c2 = colors[0], colors[-1]
    fill = (
        rnd.randint(min(c1[0], c2[0]), max(c1[0], c2[0])),
        rnd.randint(min(c1[1], c2[1]), max(c1[1], c2[1])),
        rnd.randint(min(c1[2], c2[2]), max(c1[2], c2[2])),
    )

    stroke_c1, stroke_c2 = stroke_colors[0], stroke_colors[-1]

    stroke_fill = (
        rnd.randint(min(stroke_c1[0], stroke_c2[0]), max(stroke_c1[0], stroke_c2[0])),
        rnd.randint(min(stroke_c1[1], stroke_c2[1]), max(stroke_c1[1], stroke_c2[1])),
        rnd.randint(min(stroke_c1[2], stroke_c2[2]), max(stroke_c1[2], stroke_c2[2])),
    )
    return fill, stroke_fill
