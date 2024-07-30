from ossapi import Ossapi, Score
import os
from dotenv import find_dotenv, load_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# Get osu! api
api = Ossapi(CLIENT_ID, CLIENT_SECRET)

# Returns the score object
def get_score(score_link: str):

    # Specify gamemode of score
    match score_link:
        case link if "/osu/" in link:
            id = int(score_link[30:])
            score = api.score_mode("osu", id)
        case link if "/taiko/" in link:
            id = int(score_link[32:])
            score = api.score_mode("taiko", id)
        case link if "/mania/" in link:
            id = int(score_link[32:])
            score = api.score_mode("mania", id)
        case link if "/fruits/" in link:
            id = int(score_link[33:])
            score = api.score_mode("fruits", id)
        case _:
            id = int(score_link[26:])
            score = api.score(id)
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

