from PIL import Image, ImageDraw, ImageFont, ImageEnhance, UnidentifiedImageError

import requests
import random
import time
import os
import uuid

from util.score import ScoreInfo
from util.ranking_panel import (
    ranking_panel_fruits,
    ranking_panel_mania,
    ranking_panel_osu,
    ranking_panel_taiko,
)
from util.screenshot_util import skin_dir, resize_image

# Scorepost generator images directory, skin and assets paths
scorepost = os.path.dirname(os.path.abspath(__file__))
scorepost_generator_dir = os.path.join(
    scorepost, "static", "scorepost_generator_images"
)
assets_dir = os.path.join(scorepost, "util", "assets")
skin_dir = os.path.join(assets_dir, "skin")


def set_up_image_dimensions(im: Image.Image):
    """Returns a copy of im with 1920/1080 ratio

    Args:
        im (Image.Image): Image

    Returns:
        _type_: _description_
    """

    # Constants of dimensions and ratio
    DESIRED_WIDTH = 1920
    DESIRED_HEIGHT = 1080
    DESIRED_RATIO = DESIRED_WIDTH / DESIRED_HEIGHT

    # Image current dimensions and ratio
    width, height = im.size
    current_ratio = width / height

    # Crop im to be 1920/1080 ratio to prevent stretching
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
    """Pastes the skeleton according to the gamemode of the score

    Args:
        im (Image.Image): _description_
        score (ScoreInfo): _description_
    """

    match score.mode.value:
        # Osu gamemode has different skeleton whether it has a replay or not
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
    """Writes s onto im on coordinates xy with font size of font_size and
    Aller font

    Args:
        s (str): String
        xy (tuple): Coordinates
        font_size (int): Font size
        im (Image): Image
    """
    # Write onto image
    draw_text = ImageDraw.Draw(im)
    myFont = ImageFont.truetype(os.path.join(assets_dir, "Aller_Lt.ttf"), font_size)
    draw_text.text(xy, s, font=myFont, fill=(255, 255, 255))


def generate_top_left_text(im: Image.Image, score: ScoreInfo):
    """Generates the score's beatmap title, artist, version, and creator.
    As well as the score's player, and the date and time the play was set


    Args:
        im (Image.Image): Image
        score (ScoreInfo): Score
    """

    # Initialize the string to be drawn
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

    # For datetime, it is after player, so calculate player text size
    size = ImageDraw.Draw(im)
    font_path = os.path.join(assets_dir, "Aller_Lt.ttf")
    myFont_medium = ImageFont.truetype(font_path, 30)
    datetime_position_left = (
        size.textlength(player, font=myFont_medium, font_size=30) + 15
    )

    # Write onto image
    aller_write_on_img(datetime, (datetime_position_left, 97), 25, im)
    aller_write_on_img(title, (10, 10), 45, im)
    aller_write_on_img(creator, (13, 60), 30, im)
    aller_write_on_img(player, (13, 94), 30, im)


def generate_mods_items(im: Image.Image, score: ScoreInfo):
    """Paste mods onto image

    Args:
        im (Image.Image): Image
        score (ScoreInfo): Score
    """

    # Initialize score mods, if NM then no need to paste anything
    mods = f"{score.mods}"
    if mods == "NM":
        return

    # Mods dictionary with corresponding image
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

    # mods will be one long string, so divide the string
    # into an array with every 2 characters to get each mod name.
    # Then create an array for the corresponding image file names
    mods_array = [mods[i : i + 2] for i in range(0, len(mods), 2)]
    mods_img_arr = [mods_img_dict[m] for m in mods_array]

    RIGHT = 50  # Amount of spacing between each mod image

    # Paste each mod image onto image
    for n in mods_img_arr:
        mod_img = Image.open(os.path.join(skin_dir, "Aristia(Edit)", n))
        mod_img = resize_image(mod_img, 0.7)
        im.paste(mod_img, (1834 - RIGHT, 550), mod_img)
        RIGHT += 50


def generate_rank(im: Image.Image, score: ScoreInfo):
    """Paste the rank of the score onto im

    Args:
        im (Image.Image): Image
        score (ScoreInfo): Score
    """
    # Initialize score rank and dictionary
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

    # Skin directory
    skin_folder = os.path.join(skin_dir, "Aristia(Edit)")

    # Initialize corresponding rank image, resize and paste onto im
    rank_img = Image.open(os.path.join(skin_folder, rank_img_dict[rank]))
    rank_img = resize_image(rank_img, 0.7)
    im.paste(rank_img, (1460, 260), rank_img)


def ranking_panel(im: Image.Image, score: ScoreInfo):
    """Pastes ranking panel information onto im

    Args:
        im (Image.Image): Image
        score (ScoreInfo): Score
    """

    # Different gamemodes has different statistics to display
    score_mode = score.mode.value
    if score_mode == "osu":
        ranking_panel_osu(im, score)
    elif score_mode == "mania":
        ranking_panel_mania(im, score)
    elif score_mode == "taiko":
        ranking_panel_taiko(im, score)
    elif score_mode == "fruits":
        ranking_panel_fruits(im, score)


def generate_screenshot(score: ScoreInfo):
    """Generates a screenshot of the scorepost

    Args:
        score (ScoreInfo): Score

    Returns:
        str: The name of the file of the screenshot
    """

    # Initialize screenshot file name
    random_id = str(uuid.uuid4())  # Unique name for each screenshot
    screenshot_file_name = f"score{random_id}.jpg"

    # Get beatmapset background data from link
    beatmapset_id = score.beatmapset_id
    beatmap_img_url = f"https://assets.ppy.sh/beatmaps/{beatmapset_id}/covers/raw.png"
    img_data = requests.get(beatmap_img_url).content

    # Path to screenshots directory
    path_to_screenshot_dir = os.path.join(scorepost_generator_dir, "screenshots")
    path_to_background = os.path.join(
        scorepost_generator_dir, "backgrounds", f"background{random_id}.jpg"
    )
    with open(path_to_background, "wb") as handler:
        handler.write(img_data)

    # If the link does not return any data for the background, it could be that it is
    # not a png file, so try again for jpg. If it does not return any data again, then
    # assume that the beatmapset has no background, so the background file is a random choice
    # in default_background directory.
    try:
        im = Image.open(path_to_background)
    except UnidentifiedImageError:
        beatmap_img_url = f"https://assets.ppy.sh/beatmaps/{beatmapset_id}/covers/raw.jpg"  # Try with jpg
        img_data = requests.get(beatmap_img_url).content
        with open(path_to_background, "wb") as handler:
            handler.write(img_data)
        try:
            im = Image.open(path_to_background)
        except UnidentifiedImageError:
            # If it doesn't work, pick a random default background
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

    # Dim beatmap background
    im = im.convert("RGB")
    color_enhancer = ImageEnhance.Color(im)
    brightness_enhance = ImageEnhance.Brightness(im)
    im = color_enhancer.enhance(0.50)
    im = brightness_enhance.enhance(0.6)

    # Set up image dimensions and paste skeleton
    im = set_up_image_dimensions(im)
    set_up_skeleton(im, score)

    # Paste score information
    generate_top_left_text(im, score)
    generate_rank(im, score)
    generate_mods_items(im, score)
    ranking_panel(im, score)

    # Delete the saved background file
    os.remove(path_to_background)

    # Delete all previous screenshot files that are older than 1 hour
    for ss in os.listdir(path_to_screenshot_dir):
        past_screenshot = os.path.join(path_to_screenshot_dir, ss)
        if time.time() - os.path.getmtime(past_screenshot) > (60 * 60):
            print("Removing past screenshots")
            os.remove(past_screenshot)

    # Save the screenshot and return the file name
    im.save(os.path.join(scorepost_generator_dir, "screenshots", screenshot_file_name))
    return screenshot_file_name
