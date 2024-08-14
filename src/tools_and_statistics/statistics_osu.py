from ossapi import Score
import os
import sys
from multiprocessing import Process
statistics_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(statistics_dir, "..")
sys.path.append(parent_dir)
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from osu_api import get_score, count_geki_katu_osu
from ss_generator_tools import write_with_img, skin_dir

def generate_statistics_osu(im: Image.Image, score: Score):
    count_300 = f"{score.statistics.count_300}"
    count_100 = f"{score.statistics.count_100}"
    count_50 = f"{score.statistics.count_50}"
    count_miss = f"{score.statistics.count_miss}"

    accuracy = f"{score.accuracy * 100 :.2f}%"
    max_combo = f"{score.max_combo}"

    if score.id == score.best_id:
        count_300k_100k = count_geki_katu_osu(score)
        count_100k = f"{count_300k_100k["count_100k"]}"
        count_300k = f"{count_300k_100k["count_300k"]}"
        write_with_img(count_300k, 608, 325, 1.5, im)
        write_with_img(count_100k, 608, 455, 1.5, im)   

    write_with_img(count_300, 180, 325, 1.5, im)
    write_with_img(count_100, 180, 455, 1.5, im)
    write_with_img(count_50, 180, 575, 1.5, im)
    write_with_img(count_miss, 608, 575, 1.5, im)
    write_with_img(max_combo, 35, 740, 1.5, im)
    write_with_img(accuracy, 440, 740, 1.5, im)