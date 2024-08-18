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

def extract_id_from_link(input: str, oss: Ossapi):
    link_parts = input.split("/")

    if link_parts[-1] == '':
        link_parts.pop()

    if len(link_parts) == 2 or len(link_parts) == 3:
        if link_parts[0] == "users":
            try:
                link_id = int(link_parts[1])
                print("got user id!")
            except ValueError:
                try:
                    user = oss.user(link_parts[1])
                    print("got username!")
                except ValueError:
                    return None
                link_id = user.id
        elif link_parts[0] == "scores":
            if len(link_parts) == 3:
                i = 2
            else:
                i = 1
            try:
                link_id = int(link_parts[i])
                print("got score id!")
            except ValueError:
                return None
        return link_id
    else:
        return None
    
def get_recent_score(user_id: int, mode:str | None, oss: Ossapi):
    try:
        if mode != None:
            recent_scores = oss.user_scores(user_id=user_id, legacy_only=False, type="recent", mode=mode, limit=1, include_fails=True)
        else:
            recent_scores = oss.user_scores(user_id=user_id, legacy_only=False, type="recent", limit=1, include_fails=True)
        print("got recent score!")
    except ValueError:
            return None
    if recent_scores != []:
        return recent_scores[0]
    else:
        print("no recent score!")
        return -1
        
def get_score_by_id(score_id: int, mode:str | None, oss: Ossapi):
    try:
        if mode != None:
            score = oss.score_mode(mode, score_id)
        else:
            score = oss.score(score_id)
        print("got score by id!")
    except ValueError:
            return None
    return score

def get_ossapi_score(input: str, oss: Ossapi):
    
    if "osu.ppy.sh/" in input:
        is_link = True
        input = input.split("osu.ppy.sh/")[1]
        link_id = extract_id_from_link(input, oss)
        if link_id == None:
            return link_id
    else:
        is_link = False
        try:
            user = oss.user(input)
            print("is not link! got username!")
        except ValueError:
             return None
        link_id = user.id
    
    if "users/" in input or is_link == False:
        if is_link == False:
            score = get_recent_score(link_id, None, oss)
        else:
            modes = {
                "/osu": "osu",
                "/taiko": "taiko",
                "/fruits": "fruits",
                "/mania": "mania"
            }
            mode = next((modes[i] for i in modes if i in input), None)
            score = get_recent_score(link_id, mode, oss)
    else:
        modes = {
            "/osu/": "osu",
            "/taiko/": "taiko",
            "/fruits/": "fruits",
            "/mania/": "mania"
        }
        mode = next((modes[i] for i in modes if i in input), None)
        score = get_score_by_id(link_id, mode, oss)
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
    try:
        rank = next(i for i, s in enumerate(score_list, start=1) if s.id == score.id)
        return rank
    except StopIteration:
        # Returns 0 if score is not in leaderboard
        return 0

    # Returns 0 if score is not in leaderboard

def get_score_info(input: str):
    oss = Ossapi(CLIENT_ID, CLIENT_SECRET)
    cg = Circleguard(API_KEY)
    score_ossapi = get_ossapi_score(input, oss)
    if score_ossapi == -1:
        return -1
    elif score_ossapi == None:
        return None
    difficulty_attributes = oss.beatmap_attributes(beatmap_id=score_ossapi.beatmap.id, mods=score_ossapi.mods, ruleset=score_ossapi.mode.value)
    
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
