import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, "..")
skin_dir = os.path.join(current_dir, "skin")
util_dir = os.path.join(current_dir, "util")
sys.path.append(current_dir)
sys.path.append(skin_dir)
sys.path.append(util_dir)
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from osu_api import get_score
import requests
from ossapi import Score

def create_score_screenshot(url):

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

    def set_up_skeleton(im: Image.Image):
        width, height = im.size
        rectangle = Image.open(os.path.join(util_dir, "black_rectangle.png")).convert('RGBA')
        ranking_panel = Image.open(os.path.join(skin_dir, "Aristia(Edit)", "ranking-panel@2x.png")).convert('RGBA')
        back_button = Image.open(os.path.join(skin_dir, "Aristia(Edit)", "menu-back-7@2x.png")).convert('RGBA')
        ranking_graph = Image.open(os.path.join(skin_dir, "Aristia(Edit)", "ranking-graph@2x.png")).convert('RGBA')
        replay_button = Image.open(os.path.join(skin_dir, "Aristia(Edit)", "pause-replay.png")).convert('RGBA')

        green_hit = Image.open(os.path.join(skin_dir, "Aristia(Edit)", "hit100.png")).convert('RGBA')
        blue_hit = Image.open(os.path.join(skin_dir, "Aristia(Edit)", "hit50.png")).convert('RGBA')
        miss = Image.open(os.path.join(skin_dir,"Aristia(Edit)", "hit0.png")).convert('RGBA')

        im.paste(rectangle, (0, 0), rectangle)
        back_button = back_button.resize((308, 174))
        ranking_panel = ranking_panel.resize((924, 980))
        im.paste(back_button, (0, height - 174), back_button)
        im.paste(ranking_panel, (0, 145), ranking_panel)
        ranking_graph = ranking_graph.resize((397, 205))
        im.paste(ranking_graph, (435, height - 225), ranking_graph)
        replay_button = replay_button.resize((546, 91))
        im.paste(replay_button, (1350, 840), replay_button)

        im.paste(green_hit, (22, 455), green_hit)
        im.paste(blue_hit, (22, 575), blue_hit)
        im.paste(green_hit, (450, 455), green_hit)
        im.paste(miss, (450, 575), miss)

    def generate_top_left_text(im: Image.Image, score : Score):
        title = score.beatmapset.artist + " - " + score.beatmapset.title + " [" + score.beatmap.version + "]"
        creator = f"Beatmap by {score.beatmapset.creator}"
        player = f"Played by {score._user.username} on "
        datetime = f"{score.created_at.strftime("%d.%m.%Y %H:%M:%S")}."

        draw_title = ImageDraw.Draw(im)
        draw_creator = ImageDraw.Draw(im)
        draw_player = ImageDraw.Draw(im)
        draw_datetime = ImageDraw.Draw(im)

        myFont_large = ImageFont.truetype(os.path.join(util_dir, 'Aller_Lt.ttf'), 45)
        myFont_medium = ImageFont.truetype(os.path.join(util_dir, 'Aller_Lt.ttf'), 30)
        myFont_medium_small = ImageFont.truetype(os.path.join(util_dir, 'Aller_Lt.ttf'), 25)

        draw_title.text((10, 10), title, font=myFont_large, fill = (255,255,255))
        draw_creator.text((13, 55), creator, font=myFont_medium, fill = (255,255,255))
        draw_player.text((13, 85), player, font=myFont_medium, fill = (255,255,255))
        size = ImageDraw.Draw(im)
        datetime_postition_left = size.textlength(player, font=myFont_medium, font_size=30) + 15
        draw_datetime.text((datetime_postition_left, 90), datetime, font=myFont_medium_small, fill = (255, 255, 255))
    
    def generate_mods_items(im : Image.Image, score: Score):
        mods = f"{score.mods}"
        if mods == "NM":
            return
        mods_img_dict = {
            'AT' : 'selection-mod-autoplay@2x.png',
            'CM' : 'selection-mod-cinema@2x.png',
            'EZ' : 'selection-mod-easy@2x.png',
            'DT' : 'selection-mod-doubletime@2x.png',
            'FI' : 'selection-mod-fadein@2x.png',
            'FL' : 'selection-mod-flashlight@2x.png',
            'HT' : 'selection-mod-halftime@2x.png',
            'HR' : 'selection-mod-hardrock@2x.png',
            'HD' : 'selection-mod-hidden@2x.png',
            '1K' : 'selection-mod-key1@2x.png',
            '2K' : 'selection-mod-key2@2x.png',
            '3K' : 'selection-mod-key3@2x.png',
            '4K' : 'selection-mod-key4@2x.png',
            '5K' : 'selection-mod-key5@2x.png',
            '6K' : 'selection-mod-key6@2x.png',
            '7K' : 'selection-mod-key7@2x.png',
            '8K' : 'selection-mod-key8@2x.png',
            '9K' : 'selection-mod-key9@2x.png',
            'CP' : 'selection-mod-keycoop@2x.png',
            'NC' : 'selection-mod-nightcore@2x.png',
            'NF' : 'selection-mod-nofail@2x.png',
            'PF' : 'selection-mod-perfect@2x.png',
            'RD' : 'selection-mod-random@2x.png',
            'RL' : 'selection-mod-relax@2x.png',
            'AP' : 'selection-mod-relax2@2x.png',
            'SO' : 'selection-mod-spunout@2x.png',
            'SD' : 'selection-mod-suddendeath@2x.png',
            'TP' : 'selection-mod-target@2x.png',
        }
        
        mods_array = [mods[i:i+2] for i in range(0, len(mods), 2)]

        mods_img_arr = []
        for m in mods_array:
            mods_img_arr.append(mods_img_dict[m])
        
        right = 50
        for n in mods_img_arr:
            mod_img =  Image.open(os.path.join(skin_dir, "Aristia(Edit)", n))
            mod_img = mod_img.resize((109, 106))
            im.paste(mod_img, (1834 - right, 550), mod_img)
            right += 50
        print(mods_img_arr)
        print(mods_array)

    def generate_rank(im: Image.Image, score: Score):
        rank = f"{score.rank.value}"
        rank_img_dict = {
            "A" : "Ranking-A@2x.png",
            "B" : "Ranking-B@2x.png",
            "C" : "Ranking-C@2x.png",
            "D" : "Ranking-D@2x.png",
            "S" : "Ranking-S@2x.png",
            "SH" : "Ranking-SH@2x.png",
            "X" : "Ranking-X@2x.png",
            "XH" : "Ranking-XH@2x.png",
        }
        skin_folder = os.path.join(skin_dir,"Aristia(Edit)")
        rank_img = Image.open(os.path.join(skin_folder, rank_img_dict[rank]))
        rank_img = rank_img.resize((378, 491))
        im.paste(rank_img, (1460, 260), rank_img)


    def generate_statistics(im: Image.Image, score: Score):
        def write_with_font(s: str, x: int, y: int, size: float):
            char_width = 25
            char_height = 35
            dot_width = 15
            dot_height = 35
            percent_width = 33
            percent_height = 35
            letters_dict = {
                '0' : "berlin-0.png",
                '1' : "berlin-1.png",
                '2' : "berlin-2.png",
                '3' : "berlin-3.png",
                '4' : "berlin-4.png",
                '5' : "berlin-5.png",
                '6' : "berlin-6.png",
                '7' : "berlin-7.png",
                '8' : "berlin-8.png",
                '9' : "berlin-9.png",
                '.' : "berlin-dot.png",
                '%' : "berlin-percent.png",
            }
            path = os.path.join(skin_dir, "Aristia(Edit)", "num/")
            left = 0
            space_size = 25
            #print(f"{s} : {x + left}")

            if s == "None":
                char_img =  Image.open(os.path.join(path, letters_dict['0']))
                char_img = char_img.resize((round(char_width * size), round(char_height * size)))
                im.paste(char_img, (x + left, y), char_img)
            else:
                for char in s:
                    char_img =  Image.open(os.path.join(path + letters_dict[char]))
                    if char == '.':
                        char_img = char_img.resize((round(dot_width * size), round(dot_height * size)))
                        im.paste(char_img, (x + left, y), char_img)
                        space_size = space_size - 11
                        left += round(space_size * size)
                    elif char == '%':
                        char_img = char_img.resize((round(percent_width * size), round(percent_height * size)))
                        im.paste(char_img, (x + left, y), char_img)
                        left += round(space_size * size)
                    else:
                        char_img = char_img.resize((round(char_width * size), round(char_height * size)))
                        im.paste(char_img, (x + left, y), char_img)
                        if space_size != 25:
                            space_size = 25
                        left += round(space_size * size)
                    #print(x)

        score_amount = score.score
        score_amount_str = f"{score_amount}"
        if score_amount < 10000000:
            score_amount_str = ("0" * (8 - len(score_amount_str))) + score_amount_str

        count_300 = f"{score.statistics.count_300}"
        count_300k = f"{score.statistics.count_geki}"
        count_100 = f"{score.statistics.count_100}"
        count_100k = f"{score.statistics.count_katu}"
        count_50 = f"{score.statistics.count_50}"
        count_miss = f"{score.statistics.count_miss}"

        accuracy = f"{score.accuracy * 100 :.2f}%"
        max_combo = f"{score.max_combo}"
        write_with_font(score_amount_str, 265, 180, 1.8)
        write_with_font(count_300, 180, 325, 1.5)
        write_with_font(count_300k, 608, 325, 1.5)
        write_with_font(count_100, 180, 455, 1.5)
        write_with_font(count_50, 180, 575, 1.5)
        write_with_font(count_100k, 608, 455, 1.5)
        print(count_100k)
        write_with_font(count_miss, 608, 575, 1.5)
        print(count_miss)
        write_with_font(max_combo, 35, 740, 1.5)
        write_with_font(accuracy, 440, 740, 1.5)
        #draw_percentage.text((1000, 700), "100.00%", font=myFont_large, fill = (255,255,255))
    
    score = get_score(url)
    beatmapset_id = score.beatmapset.id
    beatmap_img_url = f"https://assets.ppy.sh/beatmaps/{beatmapset_id}/covers/raw.jpg"
    img_data = requests.get(beatmap_img_url).content

    with open(os.path.join(current_dir, "..", "flaskr", "static", "background.png"), 'wb') as handler:
        handler.write(img_data)
    im = Image.open(os.path.join(parent_dir, "flaskr", "static", "background.png"))
    color_enhancer = ImageEnhance.Color(im)
    brightness_enhance = ImageEnhance.Brightness(im)

    im = color_enhancer.enhance(0.50)
    im = brightness_enhance.enhance(0.7)
    im = set_up_image_dimensions(im)
    set_up_skeleton(im)
    generate_top_left_text(im, score)
    generate_rank(im, score)
    generate_mods_items(im, score)
    generate_statistics(im, score)

    im.save(os.path.join(current_dir, "..", "flaskr", "static", "score.png"))
    print("Success!")

#create_score_screenshot("https://osu.ppy.sh/scores/627260661")
#create_score_screenshot("https://osu.ppy.sh/scores/3002498362")
#create_score_screenshot("https://osu.ppy.sh/scores/329583391")
#create_score_screenshot("https://osu.ppy.sh/scores/1715153265")