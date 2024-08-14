from ossapi import Ossapi, Score
from circleguard import Circleguard, ReplayMap
import os
import re
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
API_KEY = os.getenv("API_KEY")
# Get osu! api
api = Ossapi(CLIENT_ID, CLIENT_SECRET)
cg = Circleguard(API_KEY)

# Returns the score object
def get_score(input: str):
    # Sets id whether the input is a link or not
    if "osu.ppy.sh/" in input:
         # If it is a link, the id would be the number inside of the link
         is_link = True
         link_id = int(re.search(r'\d+', input).group())
    else:
         # Assume the input is a username
         is_link = False
         user = api.user(input)
         link_id = user.id

    # Search by score or user
    if "/users/" in input or is_link == False:
          if "/osu" in input:
                recent_scores = api.user_scores(user_id=link_id, legacy_only=False, type="recent", mode="osu", limit=1, include_fails=True)
                if recent_scores != []:
                     score = recent_scores[0]
                else:
                     score = None
          elif "/taiko" in input:
                recent_score = api.user_scores(user_id=link_id, legacy_only=False, type="recent", mode="taiko", limit=1, include_fails=True)
                if recent_scores != []:
                     score = recent_scores[0]
                else:
                     score = None
          elif "/fruits" in input:
                recent_score = api.user_scores(user_id=link_id, legacy_only=False, type="recent", mode="fruits", limit=1, include_fails=True)
                if recent_scores != []:
                     score = recent_scores[0]
                else:
                     score = None
          elif "/mania" in input:
                recent_score = api.user_scores(user_id=link_id, legacy_only=False, type="recent", mode="mania", limit=1, include_fails=True)
                if recent_scores != []:
                     score = recent_scores[0]
                else:
                     score = None
          else:
                recent_scores = api.user_scores(user_id=link_id, legacy_only=False, type="recent", include_fails=True)
                if recent_scores != []: 
                    score = recent_scores[0]
                else:
                     score = None

    elif "/osu/" in input:
        score = api.score_mode("osu", link_id)
    elif "/taiko/" in input:
        score = api.score_mode("taiko", link_id)
    elif "/mania/" in input:
        score = api.score_mode("mania", link_id)
    elif "/fruits/" in input:
        score = api.score_mode("fruits", link_id)
    else:
        score = api.score(link_id)

    if score == None:
        print("ERROR NO SCORE FOUND")
    return score

# Returns difficulty attributes of score
def get_difficulty_attributes(score: Score):
    return api.beatmap_attributes(score.beatmap.id, mods=score.mods, ruleset=score.mode.value)

# Calculates global ranking of score in a beatmap
def get_ranking_global(score: Score):

    # Lists of scores on a beatmap with proper leaderboard order
    scores = api.beatmap_scores(beatmap_id=score.beatmap.id, legacy_only=True, mode=score.mode.value)
    score_list = scores.scores

    # Calculate ranking by iterating through list of scores
    rank = 0
    for s in score_list:
        rank += 1
        if s.id == score.id:
            return rank
    
    # Returns 0 if score is not in leaderboard
    return 0

def count_geki_katu_osu(score : Score):
    replay = ReplayMap(score.beatmap.id, score.user_id)
    cg.load(replay)
    return {
        "count_300k" : f"{replay.count_geki}",
        "count_100k" : f"{replay.count_katu}"
    }

def get_beatmap(id : int):
     return api.beatmap(beatmap_id=id)