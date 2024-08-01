from ossapi import Score
import os
import sys
statistics_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(statistics_dir, "..")
sys.path.append(parent_dir)
from PIL import Image
from ss_generator_tools import resize_image, write_with_img, skin_dir, util_dir

def generate_statistics_mania(im: Image.Image, score: Score):
    count_300 = f"{score.statistics.count_300}"
    count_100 = f"{score.statistics.count_100}"
    count_50 = f"{score.statistics.count_50}"
    count_miss = f"{score.statistics.count_miss}"
    count_100k = f"{score.statistics.count_katu}"
    count_300k = f"{score.statistics.count_geki}"

    accuracy = f"{score.accuracy * 100 :.2f}%"
    max_combo = f"{score.max_combo}"

    hit_max = Image.open(os.path.join(skin_dir, "Aristia(Edit)", "mania-hit300g-0@2x.png")).convert('RGBA')
    hit_300 = Image.open(os.path.join(skin_dir, "Aristia(Edit)", "mania-hit300@2x.png")).convert('RGBA')
    hit_200 = Image.open(os.path.join(skin_dir, "Aristia(Edit)", "mania-hit200@2x.png")).convert('RGBA')
    hit_100 = Image.open(os.path.join(skin_dir, "Aristia(Edit)", "mania-hit100@2x.png")).convert('RGBA')
    hit_50 = Image.open(os.path.join(skin_dir, "Aristia(Edit)", "mania-hit50@2x.png")).convert('RGBA')
    miss = Image.open(os.path.join(skin_dir, "Aristia(Edit)", "mania-hit0@2x.png")).convert('RGBA')

    hit_max = resize_image(hit_max, 0.35)
    hit_300 = resize_image(hit_300, 0.35)
    hit_200 = resize_image(hit_200, 0.4)
    hit_100 = resize_image(hit_100, 0.4)
    hit_50 = resize_image(hit_50, 0.5)
    miss = resize_image(miss, 0.4)

    im.paste(hit_max, (425, 345), hit_max)
    im.paste(hit_300, (5, 345), hit_300)
    im.paste(hit_200, (40, 470), hit_200)
    im.paste(hit_100, (465, 470), hit_100)
    im.paste(hit_50, (50, 588), hit_50)
    im.paste(miss, (470, 588), miss)

    write_with_img(count_300k, 608, 325, 1.5, im)
    write_with_img(count_100k, 608, 455, 1.5, im)
    write_with_img(count_300, 180, 325, 1.5, im)
    write_with_img(count_100, 180, 455, 1.5, im)
    write_with_img(count_50, 180, 575, 1.5, im)
    write_with_img(count_miss, 608, 575, 1.5, im)
    write_with_img(max_combo, 35, 740, 1.5, im)
    write_with_img(accuracy, 440, 740, 1.5, im)

#print(get_score("https://osu.ppy.sh/scores/2344387027").statistics)

