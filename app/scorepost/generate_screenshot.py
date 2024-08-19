import os
import uuid

scorepost = os.path.dirname(os.path.abspath(__file__))
scorepost_generator_dir = os.path.join(
    scorepost, "..", "static", "scorepost_generator_images"
)
assets_dir = os.path.join(scorepost, "assets")
skin_dir = os.path.join(assets_dir, "skin")

from PIL import Image, ImageDraw, ImageFont, ImageEnhance, UnidentifiedImageError

import requests
import random
import time

from .util.score import ScoreInfo
from .util.screenshot_util import skin_dir, resize_image, write_with_img
from .util.statistics_fruits import generate_statistics_fruits
from .util.statistics_osu import generate_statistics_osu
from .util.statistics_taiko import generate_statistics_taiko
from .util.statistics_mania import generate_statistics_mania


def set_up_image_dimensions(im: Image.Image):
    DESIRED_WIDTH = 1920
    DESIRED_HEIGHT = 1080
    DESIRED_RATIO = DESIRED_WIDTH / DESIRED_HEIGHT

    width, height = im.size
    current_ratio = width / height

    if current_ratio > DESIRED_RATIO:
        new_width = round(DESIRED_RATIO * height)
        new_height = height
        difference = abs(width - new_width)
        im = im.crop((difference // 2, 0, width - difference // 2, height))
    else:
        new_height = round(width * (DESIRED_HEIGHT / DESIRED_WIDTH))
        new_width = width
        difference = abs(height - new_height)
        im = im.crop((0, difference // 2, width, height - difference // 2))

    im = im.resize((DESIRED_WIDTH, DESIRED_HEIGHT), Image.Resampling.BICUBIC)
    return im


def set_up_skeleton(im: Image.Image, score: ScoreInfo):
    match score.mode.value:
        case "osu":
            if score.id == score.best_id:
                skeleton = Image.open(
                    os.path.join(
                        skin_dir,
                        "Aristia(Edit)",
                        "skeletons",
                        "osu_replay_skeleton.png",
                    )
                )
            else:
                skeleton = Image.open(
                    os.path.join(
                        skin_dir,
                        "Aristia(Edit)",
                        "skeletons",
                        "osu_noreplay_skeleton.png",
                    )
                )
        case "taiko":
            skeleton = Image.open(
                os.path.join(
                    skin_dir, "Aristia(Edit)", "skeletons", "taiko_skeleton.png"
                )
            )
        case "mania":
            skeleton = Image.open(
                os.path.join(
                    skin_dir, "Aristia(Edit)", "skeletons", "mania_skeleton.png"
                )
            )
        case "fruits":
            skeleton = Image.open(
                os.path.join(
                    skin_dir, "Aristia(Edit)", "skeletons", "fruits_skeleton.png"
                )
            )
    im = im.paste(skeleton, (0, 0), skeleton)


def aller_write_on_img(s: str, xy: tuple, font_size: int, im: Image):
    draw_text = ImageDraw.Draw(im)
    myFont = ImageFont.truetype(os.path.join(assets_dir, "Aller_Lt.ttf"), font_size)
    draw_text.text(xy, s, font=myFont, fill=(255, 255, 255))


def generate_top_left_text(im: Image.Image, score: ScoreInfo):
    title = (
        score.beatmapset_artist
        + " - "
        + score.beatmapset_title
        + " ["
        + score.beatmap_version
        + "]"
    )
    creator = f"Beatmap by {score.beatmapset_creator}"
    player = f"Played by {score.username} on "
    datetime = f'{score.created_at.strftime("%d.%m.%Y %H:%M:%S")}.'

    draw_datetime = ImageDraw.Draw(im)

    aller_write_on_img(title, (10, 10), 45, im)
    aller_write_on_img(creator, (13, 60), 30, im)
    aller_write_on_img(player, (13, 94), 30, im)

    size = ImageDraw.Draw(im)
    font_path = os.path.join(assets_dir, "Aller_Lt.ttf")
    myFont_medium = ImageFont.truetype(font_path, 30)
    datetime_postition_left = (
        size.textlength(player, font=myFont_medium, font_size=30) + 15
    )
    f = ImageFont.truetype(font_path, 25)
    draw_datetime.text(
        (datetime_postition_left, 97), datetime, font=f, fill=(255, 255, 255)
    )


def generate_mods_items(im: Image.Image, score: ScoreInfo):
    mods = f"{score.mods}"
    if mods == "NM":
        return
    mods_img_dict = {
        "AT": "selection-mod-autoplay@2x.png",
        "CM": "selection-mod-cinema@2x.png",
        "EZ": "selection-mod-easy@2x.png",
        "DT": "selection-mod-doubletime@2x.png",
        "FI": "selection-mod-fadein@2x.png",
        "FL": "selection-mod-flashlight@2x.png",
        "HT": "selection-mod-halftime@2x.png",
        "HR": "selection-mod-hardrock@2x.png",
        "HD": "selection-mod-hidden@2x.png",
        "1K": "selection-mod-key1@2x.png",
        "2K": "selection-mod-key2@2x.png",
        "3K": "selection-mod-key3@2x.png",
        "4K": "selection-mod-key4@2x.png",
        "5K": "selection-mod-key5@2x.png",
        "6K": "selection-mod-key6@2x.png",
        "7K": "selection-mod-key7@2x.png",
        "8K": "selection-mod-key8@2x.png",
        "9K": "selection-mod-key9@2x.png",
        "CP": "selection-mod-keycoop@2x.png",
        "NC": "selection-mod-nightcore@2x.png",
        "NF": "selection-mod-nofail@2x.png",
        "PF": "selection-mod-perfect@2x.png",
        "RD": "selection-mod-random@2x.png",
        "RL": "selection-mod-relax@2x.png",
        "AP": "selection-mod-relax2@2x.png",
        "SO": "selection-mod-spunout@2x.png",
        "SD": "selection-mod-suddendeath@2x.png",
        "TP": "selection-mod-target@2x.png",
    }

    mods_array = [mods[i : i + 2] for i in range(0, len(mods), 2)]
    mods_img_arr = [mods_img_dict[m] for m in mods_array]

    RIGHT = 50
    for n in mods_img_arr:
        mod_img = Image.open(os.path.join(skin_dir, "Aristia(Edit)", n))
        mod_img = resize_image(mod_img, 0.7)
        im.paste(mod_img, (1834 - RIGHT, 550), mod_img)
        RIGHT += 50


def generate_rank(im: Image.Image, score: ScoreInfo):
    rank = f"{score.rank}"
    rank_img_dict = {
        "A": "Ranking-A@2x.png",
        "B": "Ranking-B@2x.png",
        "C": "Ranking-C@2x.png",
        "D": "Ranking-D@2x.png",
        "S": "Ranking-S@2x.png",
        "SH": "Ranking-SH@2x.png",
        "X": "Ranking-X@2x.png",
        "XH": "Ranking-XH@2x.png",
        "F": "Ranking-D@2x.png",
    }
    skin_folder = os.path.join(skin_dir, "Aristia(Edit)")
    rank_img = Image.open(os.path.join(skin_folder, rank_img_dict[rank]))
    rank_img = rank_img.resize((378, 491))
    im.paste(rank_img, (1460, 260), rank_img)


def generate_statistics(im: Image.Image, score: ScoreInfo):
    score_amount = score.score
    score_amount_str = f"{score_amount}"
    score_mode = score.mode.value

    if score_amount < 10000000:
        if score_mode == "mania":
            score_amount_str = ("0" * (7 - len(score_amount_str))) + score_amount_str
        else:
            score_amount_str = ("0" * (8 - len(score_amount_str))) + score_amount_str

    write_with_img(score_amount_str, 265, 180, 1.8, im)
    if score_mode == "osu":
        generate_statistics_osu(im, score)
    elif score_mode == "mania":
        generate_statistics_mania(im, score)
    elif score_mode == "taiko":
        generate_statistics_taiko(im, score)
    elif score_mode == "fruits":
        generate_statistics_fruits(im, score)


def generate_ss(score: ScoreInfo):
    beatmapset_id = score.beatmapset_id
    beatmap_img_url = f"https://assets.ppy.sh/beatmaps/{beatmapset_id}/covers/raw.png"
    random_id = str(uuid.uuid4())
    screenshot_file_name = f"score{random_id}.jpg"

    img_data = requests.get(beatmap_img_url).content
    path_to_screenshot_dir = os.path.join(scorepost_generator_dir, "screenshots")
    path_to_background = os.path.join(
        scorepost_generator_dir, "backgrounds", f"background{random_id}.jpg"
    )
    with open(path_to_background, "wb") as handler:
        handler.write(img_data)

    try:
        im = Image.open(path_to_background)
    except UnidentifiedImageError:
        beatmap_img_url = (
            f"https://assets.ppy.sh/beatmaps/{beatmapset_id}/covers/raw.jpg"
        )
        img_data = requests.get(beatmap_img_url).content
        with open(path_to_background, "wb") as handler:
            handler.write(img_data)
        try:
            im = Image.open(path_to_background)
        except UnidentifiedImageError:
            path_to_default_background_dir = os.path.join(
                scorepost_generator_dir, "default_background"
            )
            random_background = random.choice(
                os.listdir(path_to_default_background_dir)
            )
            path_to_random_background = os.path.join(
                path_to_default_background_dir, random_background
            )
            im = Image.open(path_to_random_background)

    im = im.convert("RGB")
    color_enhancer = ImageEnhance.Color(im)
    brightness_enhance = ImageEnhance.Brightness(im)
    im = color_enhancer.enhance(0.50)
    im = brightness_enhance.enhance(0.6)
    im = set_up_image_dimensions(im)
    set_up_skeleton(im, score)
    generate_top_left_text(im, score)
    generate_rank(im, score)
    generate_mods_items(im, score)
    generate_statistics(im, score)

    os.remove(path_to_background)
    for ss in os.listdir(path_to_screenshot_dir):
        past_screenshot = os.path.join(path_to_screenshot_dir, ss)
        if time.time() - os.path.getmtime(past_screenshot) > (60 * 60):
            os.remove(past_screenshot)
            print("removed file!")
    im.save(os.path.join(scorepost_generator_dir, "screenshots", screenshot_file_name))
    return screenshot_file_name
