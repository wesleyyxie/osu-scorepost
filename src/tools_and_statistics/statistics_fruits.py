from ossapi import Score
import os
import sys
from PIL import Image, ImageEnhance
statistics_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(statistics_dir, "..")
sys.path.append(parent_dir)
from ss_generator_tools import resize_image, write_with_img, skin_dir

def tint (im: Image.Image, c: tuple):
    color_img = Image.new('RGB', im.size, c)
    alpha = im.split()[3]
    return Image.composite(color_img, im, alpha)

def generate_statistics_fruits(im: Image.Image, score: Score):
    count_300 = f"{score.statistics.count_300}"
    count_100 = f"{score.statistics.count_100}"
    count_50 = f"{score.statistics.count_50}"
    count_miss = f"{score.statistics.count_miss}"

    accuracy = f"{score.accuracy * 100 :.2f}%"
    max_combo = f"{score.max_combo}"

    hit_300 = Image.open(os.path.join(skin_dir, "Aristia(Edit)", "fruit-orange@2x.png")).convert('RGBA')
    orange_overlay = Image.open(os.path.join(skin_dir, "Aristia(Edit)", "fruit-orange-overlay@2x.png")).convert('RGBA')
    hit_100 = Image.open(os.path.join(skin_dir, "Aristia(Edit)", "fruit-drop@2x.png")).convert('RGBA')
    hit_50 = Image.open(os.path.join(skin_dir, "Aristia(Edit)", "fruit-drop@2x.png")).convert('RGBA')
    miss = Image.open(os.path.join(skin_dir, "Aristia(Edit)", "fruit-orange@2x.png")).convert('RGBA')
    x = Image.open(os.path.join(skin_dir, "Aristia(Edit)", "hit0.png")).convert('RGBA').convert('RGBA')
    miss = miss.rotate(315, Image.Resampling.NEAREST, expand = 1)

    hit_300 = resize_image(hit_300, 0.4)
    hit_300_overlay = resize_image(orange_overlay, 0.4)
    hit_100 = resize_image(hit_100, 0.4)
    hit_50 = resize_image(hit_50, 0.3)
    miss = resize_image(miss, 0.3)
    miss_overlay = resize_image(orange_overlay, 0.3)
    miss_overlay = miss_overlay.rotate(315, Image.Resampling.NEAREST, expand = 1)
    x = resize_image(x, 0.4)

    # Composite the orange image with the original image, using the alpha channel as a mask
    hit_300 = tint(hit_300, (201, 126, 7))
    hit_100 = tint(hit_100, (68, 137, 38))
    hit_50 = tint(hit_50, (97,161,209))
    miss = tint(miss, (153, 153, 153))

    im.paste(hit_300, (45, 300), hit_300)
    im.paste(hit_300_overlay, (45, 300), hit_300_overlay)
    im.paste(hit_100, (75, 465), hit_100)
    im.paste(hit_50, (80, 588), hit_50)
    im.paste(miss, (470, 300), miss)
    im.paste(miss_overlay, (470, 300), miss_overlay)
    im.paste(x, (445, 300), x)
    
    write_with_img(count_300, 180, 325, 1.5, im)
    write_with_img(count_100, 180, 455, 1.5, im)
    write_with_img(count_50, 180, 575, 1.5, im)
    write_with_img(count_miss, 608, 325, 1.5, im)
    write_with_img(max_combo, 35, 740, 1.5, im)
    write_with_img(accuracy, 440, 740, 1.5, im)

#print(get_score("https://osu.ppy.sh/scores/2344387027").statistics)

