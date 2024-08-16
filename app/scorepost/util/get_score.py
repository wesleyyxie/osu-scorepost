from ossapi import Ossapi, Score
from circleguard import Circleguard, ReplayMap
import rosu_pp_py as rosu
import requests
import os
import re

from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
API_KEY = os.getenv("API_KEY")

from .score import ScoreInfo

def get_ossapi_score(input: str, oss: Ossapi):
        # Sets id whether the input is a link or not
    if "osu.ppy.sh/" in input:
         # If it is a link, the id would be the number inside of the link
         is_link = True
         link_id = int(re.search(r'\d+', input).group())
         input = input.split("osu.ppy.sh")[1]
    else:
         # Assume the input is a username
         is_link = False
         user = oss.user(input)
         link_id = user.id
    # Search by score or user
    if "/users/" in input or is_link == False:
          if "/osu" in input:
                recent_scores = oss.user_scores(user_id=link_id, legacy_only=False, type="recent", mode="osu", limit=1, include_fails=True)
                if recent_scores != []:
                     score = recent_scores[0]
                else:
                     score = None
          elif "/taiko" in input:
                print("hi")
                recent_scores = oss.user_scores(user_id=link_id, legacy_only=False, type="recent", mode="taiko", limit=1, include_fails=True)
                if recent_scores != []:
                     score = recent_scores[0]
                else:
                     score = None
          elif "/fruits" in input:
                recent_scores = oss.user_scores(user_id=link_id, legacy_only=False, type="recent", mode="fruits", limit=1, include_fails=True)
                if recent_scores != []:
                     score = recent_scores[0]
                else:
                     score = None
          elif "/mania" in input:
                recent_scores = oss.user_scores(user_id=link_id, legacy_only=False, type="recent", mode="mania", limit=1, include_fails=True)
                if recent_scores != []:
                     score = recent_scores[0]
                else:
                     score = None
          else:
                recent_scores = oss.user_scores(user_id=link_id, legacy_only=False, type="recent", include_fails=True)
                if recent_scores != []: 
                    score = recent_scores[0]
                else:
                     score = None

    elif "/osu/" in input:
        score = oss.score_mode("osu", link_id)
    elif "/taiko/" in input:
        score = oss.score_mode("taiko", link_id)
    elif "/mania/" in input:
        score = oss.score_mode("mania", link_id)
    elif "/fruits/" in input:
        score = oss.score_mode("fruits", link_id)
    else:
        score = oss.score(link_id)

    if score == None:
        print("ERROR NO SCORE FOUND")
        return -1
    return score

def count_geki_katu_osu(score: Score, beatmap_id : int, user_id : int, cg : Circleguard):
    if score.id == score.best_id:
        try:
            replay = ReplayMap(beatmap_id, user_id)
            cg.load(replay)
            return (replay.count_geki, replay.count_katu)
        except Exception:
                return (None, None)
    else:
        return (None, None)
     
def get_beatmap(id : int, oss: Ossapi):
     bm = oss.beatmap(beatmap_id=id)
     return bm

def get_difficulty_attributes(score_ossapi: Score, oss: Ossapi):
    return oss.beatmap_attributes(beatmap_id=score_ossapi.beatmap.id, mods=score_ossapi.mods, ruleset=score_ossapi.mode.value)

def get_beatmap_max_combo(map):
    diff = rosu.Difficulty()
    max_combo = diff.calculate(map).max_combo
    return max_combo

def calculate_pp(score_ossapi:  Score, map):
    number_50 = score_ossapi.statistics.count_50 or 0
    number_100 = score_ossapi.statistics.count_100 or 0
    number_misses = score_ossapi.statistics.count_miss or 0
    number_katu = score_ossapi.statistics.count_katu or 0
    number_300 = score_ossapi.statistics.count_300 or 0
    number_geki = score_ossapi.statistics.count_geki or 0

    perf_score = rosu.Performance(
        mods = score_ossapi.mods.value,
        n100 = number_100,
        n50 = number_50,
        n300 = number_300,
        n_katu = number_katu,
        n_geki = number_geki,
        combo = score_ossapi.max_combo,
        misses = number_misses,
    )
    return round(perf_score.calculate(map).pp)

def calculate_pp(score_ossapi:  Score, map):
    number_50 = score_ossapi.statistics.count_50 or 0
    number_100 = score_ossapi.statistics.count_100 or 0
    number_misses = score_ossapi.statistics.count_miss or 0
    number_katu = score_ossapi.statistics.count_katu or 0
    number_300 = score_ossapi.statistics.count_300 or 0
    number_geki = score_ossapi.statistics.count_geki or 0

    perf = rosu.Performance(
        mods = score_ossapi.mods.value,
        n100 = number_100,
        n50 = number_50,
        n300 = number_300,
        n_katu = number_katu,
        n_geki = number_geki,
    )
    pp_if_fc = round(perf.calculate(map).pp)
    perf.set_misses(number_misses)
    perf.set_combo(score_ossapi.max_combo)
    pp = round(perf.calculate(map).pp)
    return (pp, pp_if_fc)

def get_ranking_global(score: Score, oss: Ossapi):

    # Lists of scores on a beatmap with proper leaderboard order
    scores = oss.beatmap_scores(beatmap_id=score.beatmap.id, legacy_only=True, mode=score.mode.value)
    score_list = scores.scores

    # Calculate ranking by iterating through list of scores
    rank = 0
    for s in score_list:
        rank += 1
        if s.id == score.id:
            return rank
    
    # Returns 0 if score is not in leaderboard
    return 0
     
def get_score_info(input: str):
    oss = Ossapi(CLIENT_ID, CLIENT_SECRET)
    cg = Circleguard(API_KEY)
    score_ossapi = get_ossapi_score(input, oss)
    if score_ossapi == -1:
        return -1
    difficulty_attributes = get_difficulty_attributes(score_ossapi, oss)
    
    geki, katu = count_geki_katu_osu(score_ossapi, score_ossapi.beatmap.id, score_ossapi.user_id, cg)

    response = requests.get(f"https://osu.ppy.sh/osu/{score_ossapi.beatmap.id}")
    map = rosu.Beatmap(bytes = response.content)
    
    if score_ossapi.mode.value == "osu":
        map.convert(rosu.GameMode.Osu)
    elif score_ossapi.mode.value == "fruits":
        map.convert(rosu.GameMode.Catch)
    elif score_ossapi.mode.value == "taiko":
        map.convert(rosu.GameMode.Taiko)
    elif score_ossapi.mode.value == "mania":
        map.convert(rosu.GameMode.Mania)

    pp_score, pp_if_fc = calculate_pp(score_ossapi, map)

    # The max combo of beatmap only works for osu! gamemode for some reason
    beatmap_max_combo = get_beatmap_max_combo(map)

    # Needs difficulty attribute for star ratings with mods
    stars_converted = difficulty_attributes.attributes.star_rating
    global_ranking = get_ranking_global(score_ossapi, oss)

    score = ScoreInfo(
         score_ossapi=score_ossapi, geki=geki, 
         stars_converted=stars_converted, katu=katu, 
         pp=pp_score, pp_if_fc=pp_if_fc, 
         beatmap_max_combo=beatmap_max_combo, global_ranking=global_ranking)
    return score

#print(get_score("https://osu.ppy.sh/scores/3337662645"))
