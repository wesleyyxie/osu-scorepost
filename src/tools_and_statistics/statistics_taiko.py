from ossapi import Score
import os
import sys
statistics_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(statistics_dir, "..")
sys.path.append(parent_dir)
from PIL import Image
from ss_generator_tools import resize_image, write_with_img, util_dir, skin_dir
from osu_api import get_score

def generate_statistics_taiko(im: Image.Image, score: Score):
    count_300 = f"{score.statistics.count_300}"
    count_100 = f"{score.statistics.count_100}"
    count_miss = f"{score.statistics.count_miss}"

    accuracy = f"{score.accuracy * 100 :.2f}%"
    max_combo = f"{score.max_combo}"

    blue_hit = Image.open(os.path.join(skin_dir, "Aristia(Edit)", "taiko-hit300.png")).convert('RGBA')
    green_hit = Image.open(os.path.join(skin_dir, "Aristia(Edit)", "taiko-hit100.png")).convert('RGBA')
    miss = Image.open(os.path.join(skin_dir,"Aristia(Edit)", "taiko-hit0.png")).convert('RGBA')

    blue_hit = resize_image(blue_hit, 0.8)
    green_hit = resize_image(green_hit, 0.8)
    miss = resize_image(miss, 0.8)

    im.paste(blue_hit, (22, 280), blue_hit)
    im.paste(green_hit, (22, 410), green_hit)
    im.paste(miss, (22, 530), miss)

    write_with_img(count_300, 180, 325, 1.5, im)
    write_with_img(count_100, 180, 455, 1.5, im)
    write_with_img(count_miss, 180, 575, 1.5, im)
    write_with_img(max_combo, 35, 740, 1.5, im)
    write_with_img(accuracy, 440, 740, 1.5, im)