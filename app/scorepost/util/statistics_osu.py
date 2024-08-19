from PIL import Image
from .screenshot_util import write_with_img
from .get_score import count_geki_katu_osu
from .score import ScoreInfo


def generate_statistics_osu(im: Image.Image, score: ScoreInfo):
    """Write statistics, score, and accuracy for osu! gamemode
    onto ranking panel of im

    Args:
        im (Image.Image): Image
        score (ScoreInfo): Score
    """

    # Initialize info as string
    count_300 = f"{score.count_300}"
    count_100 = f"{score.count_100}"
    count_50 = f"{score.count_50}"
    count_miss = f"{score.count_miss}"

    accuracy = f"{score.accuracy * 100 :.2f}%"
    max_combo = f"{score.max_combo}"

    # Write geki and katu if available
    if score.count_geki != None and score.count_katu != None:
        count_300k = f"{score.count_geki}"
        count_100k = f"{score.count_katu}"
        write_with_img(count_300k, 608, 325, 1.5, im)
        write_with_img(count_100k, 608, 455, 1.5, im)

    # Write onto ranking panel
    write_with_img(count_300, 180, 325, 1.5, im)
    write_with_img(count_100, 180, 455, 1.5, im)
    write_with_img(count_50, 180, 575, 1.5, im)
    write_with_img(count_miss, 608, 575, 1.5, im)
    write_with_img(max_combo, 35, 740, 1.5, im)
    write_with_img(accuracy, 440, 740, 1.5, im)
