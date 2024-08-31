from util.get_score import get_ossapi_score, get_recent_score
from ossapi import Ossapi, Score
from waiting import wait

from os import getenv
from datetime import datetime
from dotenv import find_dotenv, load_dotenv

# API information from .env
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
CLIENT_ID = getenv("CLIENT_ID")
CLIENT_SECRET = getenv("CLIENT_SECRET")
API_KEY = getenv("API_KEY")


def is_next_score(user_id, current_score: Score, oss):
    next_score = get_recent_score(user_id, None, oss)
    if current_score.created_at != next_score.created_at:
        return next_score
    print(datetime.now())
    return False


oss = Ossapi(CLIENT_ID, CLIENT_SECRET)
print(f"start:{datetime.now()}")
# wait for something to be ready
# user = "sm4ko"
current_score = get_ossapi_score("sm4ko", oss)

next_score = wait(
    lambda: is_next_score(current_score.user_id, current_score, oss),
    timeout_seconds=200,
    waiting_for="something to be ready",
)
print(datetime.now())
print(next_score.created_at)
