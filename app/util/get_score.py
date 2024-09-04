from ossapi import Ossapi, Score
from circleguard import Circleguard, ReplayMap
from circleguard.loader import NoInfoAvailableException
import rosu_pp_py as rosu

from requests import get
import time
from os import getenv
from dotenv import find_dotenv, load_dotenv

from .score import ScoreInfo

# API information from .env
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
CLIENT_ID = getenv("CLIENT_ID")
CLIENT_SECRET = getenv("CLIENT_SECRET")
API_KEY = getenv("API_KEY")


def get_score_link_score(input: str, oss: Ossapi):
    """Returns the score object from a score link
    Raises ValueError if input is an invalid link

    Args:
        input (str): The link without https://osu.ppy.sh
        oss (Ossapi): Ossapi API Instance

    Raises:
        ValueError: Input in an invalid link

    Returns:
        Score: score
    """

    # Splits the link into parts based on /
    input_parts = input.split("/")
    num_of_parts = len(input_parts)

    # Link is only vaid if there are 2 or 3 parts
    if num_of_parts == 2:
        score_id = int(input_parts[1])
        return oss.score(score_id)
    elif num_of_parts == 3:
        score_id = int(input_parts[2])
        mode = input_parts[1]
        return oss.score_mode(mode=mode, score_id=score_id)
    else:
        raise ValueError


def get_score_username(input: str, oss: Ossapi):
    """Returns the the most recent score from a username

    Args:
        input (str): Username
        oss (Ossapi): Ossapi API instance

    Returns:
        Score: The user's most recent score
    """
    scores = oss.user_scores(
        user_id=oss.user(user=input).id,
        legacy_only=False,
        type="recent",
        include_fails=True,
    )
    return scores[0]


def get_user_link_score(input: str, oss: Ossapi):
    """Returns the user's most recent score from their user link

    Args:
        input (str): The link of the user
        oss (Ossapi): Ossapi API Instance

    Raises:
        ValueError: mode is invalid
        ValueError: number of parts is invalid

    Returns:
        Score: score
    """

    # Split the link based on /
    input_parts = input.split("/")
    num_of_parts = len(input_parts)

    # Only valid number of parts is 2 and 3
    if num_of_parts == 2:

        # If 2 parts, then check if the link consists of
        # a username or a userID and act accordingly
        if input_parts[1].isdigit():
            return oss.user_scores(
                user_id=int(input_parts[1]),
                legacy_only=False,
                type="recent",
                include_fails=True,
            )[0]
        else:
            return get_score_username(input_parts[1], oss)

    elif num_of_parts == 3:
        # If 3 parts, then the mode is initialized, first initialize
        # the userID based on the userlink or username if it is in the link,
        # then get the recent score
        if input_parts[1].isdigit():
            user_id = int(input_parts[1])
        else:
            user_id = oss.user(user=input_parts[1]).id
        mode = input_parts[2]
        if mode in ["osu", "taiko", "mania", "fruits"]:
            return oss.user_scores(
                user_id=user_id,
                legacy_only=False,
                type="recent",
                include_fails=True,
                mode=mode,
            )[0]
        else:
            raise ValueError
    else:
        raise ValueError


def get_ossapi_score(input: str, oss: Ossapi):
    """Get score based on the user's input. Raises
    ValueError in input is invalid

    Args:
        input (str): User's input
        oss (Ossapi): Ossapi API Instance

    Raises:
        ValueError: Input is invalid

    Returns:
        Score: score
    """

    # Check if the input is a link, otherwise assume it is a username
    if "osu.ppy.sh/" in input:
        # If / is the last character, get rid of it
        if "/" == input[-1]:
            input = input[:-1]

        # Only valid links are userlinks and score links, else raise ValueError
        if "/scores/" in input:
            return get_score_link_score(input.split("osu.ppy.sh/")[1], oss)
        elif "/users/" in input:
            return get_user_link_score(input.split("osu.ppy.sh/")[1], oss)
        else:
            raise ValueError
    else:
        return get_score_username(input, oss)


def count_geki_katu_osu(score: Score, beatmap_id: int, user_id: int, cg: Circleguard):
    """Geki and katu count are available in a replay from Circleguard. Replay is available
    if the score is the user's best score on the map. Returns a tuple of (Geki, Katu).

    Args:
        score (Score): Score object
        beatmap_id (int): Beatmap id
        user_id (int): User ID
        cg (Circleguard): Circleguard API instance

    Returns:
        Union[Tuple[int, int], Tuple[None, None]]: A tuple of geki count and katu count if
        replay is available, or else return a tuple of None
    """

    # If score is the user's best play on the map, try to get replay, else return
    # A tuple of None. It may raise a NoInfoAvailableException error so
    # return a tuple of None.
    if score.mode.value == "osu":
        if score.id == score.best_id:
            try:
                replay = ReplayMap(beatmap_id, user_id, mods=score.mods)
                cg.load(replay)
                return (replay.count_geki, replay.count_katu)
            except (
                NoInfoAvailableException
            ):  # Some replays are unavailable for some reason
                return (None, None)
        else:
            return (None, None)
    else:
        return (score.statistics.count_geki, score.statistics.count_katu)


def get_beatmap_max_combo(map: rosu.Beatmap):
    """Returns max combo of a map using rosu-pp

    Args:
        map (rosu.Beatmap): Beatmap data

    Returns:
        int: max combo of the map
    """
    diff = rosu.Difficulty()
    max_combo = diff.calculate(map).max_combo
    return max_combo


def calculate_pp(score_ossapi: Score, beatmap_max_combo: int, map: rosu.Beatmap):
    """Calculates the pp and pp if FC of a score

    Args:
        score_ossapi (Score): Score
        map (rosu.Beatmap): Beatmap data

    Returns:
        Tuple[int, int]: Tuple with pp of score, pp if FC
    """

    # If it is unranked, initialize pp with rosu, else use the score
    # object's pp count
    if not score_ossapi.pp:
        number_50 = score_ossapi.statistics.count_50 or 0
        number_100 = score_ossapi.statistics.count_100 or 0
        number_katu = score_ossapi.statistics.count_katu or 0
        number_300 = score_ossapi.statistics.count_300 or 0
        number_geki = score_ossapi.statistics.count_geki or 0
        number_miss = score_ossapi.statistics.count_miss or 0
        max_combo = score_ossapi.max_combo
        # Calculate pp of score if fc
        perf = rosu.Performance(
            mods=score_ossapi.mods.value,
            n100=number_100,
            n50=number_50,
            n300=number_300,
            n_katu=number_katu,
            n_geki=number_geki,
            misses=number_miss,
            combo=max_combo,
        )
        pp = round(perf.calculate(map).pp)
    else:
        pp = round(score_ossapi.pp)

    # If it is not FC, find if_fc_pp
    if (
        score_ossapi.max_combo <= beatmap_max_combo - 20
        or score_ossapi.statistics.count_miss > 0
    ):
        # User previous rosu perf if unranked
        if not score_ossapi.pp:
            perf.set_misses(0)
            perf.set_combo(None)
            pp_if_fc = round(perf.calculate(map).pp)
        else:
            number_50 = score_ossapi.statistics.count_50 or 0
            number_100 = score_ossapi.statistics.count_100 or 0
            number_katu = score_ossapi.statistics.count_katu or 0
            number_300 = score_ossapi.statistics.count_300 or 0
            number_geki = score_ossapi.statistics.count_geki or 0
            # Calculate pp of score if fc
            perf = rosu.Performance(
                mods=score_ossapi.mods.value,
                n100=number_100,
                n50=number_50,
                n300=number_300,
                n_katu=number_katu,
                n_geki=number_geki,
            )
            pp_if_fc = round(perf.calculate(map).pp)
    else:
        return (pp, pp)
    return (pp, pp_if_fc)


def get_ranking_global(score: Score, oss: Ossapi):
    """Returns global ranking of score in top 50

    Args:
        score (Score): Score
        oss (Ossapi): Ossapi API instance

    Returns:
        int: Global ranking or 0 if not in top 50
    """

    # Lists of scores on a beatmap with proper leaderboard order
    # Calculate ranking by iterating through list of scores
    return next(
        (
            i
            for i, s in enumerate(
                oss.beatmap_scores(
                    beatmap_id=score.beatmap.id, legacy_only=True, mode=score.mode.value
                ).scores,
                start=1,
            )
            if s.id == score.id
        ),
        0,
    )


def get_score_info(input: str):
    """Returns score information needed for screenshot and scorepost title
    from a score link, username or user link

    Args:
        input (str): User input

    Returns:
        Union[Score_Info, int]: Returns Score_Info, or
        -1 if input was a user and there are no recent scores
    """

    # Initialize Ossapi and Circleguard API
    start_time = time.time()
    st = time.time()
    oss = Ossapi(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    cg = Circleguard(API_KEY)
    print(f"api: {time.time() - st}")
    st = time.time()
    score_ossapi = get_ossapi_score(input, oss)
    print(f"score_ossapi: {time.time() - st}")
    st = time.time()
    # Difficulty attributes for calculating converted star rating
    difficulty_attributes = oss.beatmap_attributes(
        beatmap_id=score_ossapi.beatmap.id,
        mods=score_ossapi.mods,
        ruleset=score_ossapi.mode.value,
    )
    print(f"difficulty_attributes: {time.time() - st}")
    # Geki and katu counts are only available for some scores that are
    # the user's best on the map
    st = time.time()
    count_geki, count_katu = count_geki_katu_osu(
        score_ossapi, score_ossapi.beatmap.id, score_ossapi.user_id, cg
    )
    print(f"get geki katu: {time.time() - st}")
    # Get beatmap data for rosu-pp and convert to corresponding gamemode
    response = get(f"https://osu.ppy.sh/osu/{score_ossapi.beatmap.id}")
    map = rosu.Beatmap(bytes=response.content)
    if score_ossapi.mode.value == "osu":
        map.convert(rosu.GameMode.Osu)
    elif score_ossapi.mode.value == "fruits":
        map.convert(rosu.GameMode.Catch)
    elif score_ossapi.mode.value == "taiko":
        map.convert(rosu.GameMode.Taiko)
    elif score_ossapi.mode.value == "mania":
        map.convert(rosu.GameMode.Mania)

    # Limited beatmap information for recent scores so use rosu-pp
    # instead of Ossapi to get beatmap max combo
    st = time.time()
    beatmap_max_combo = get_beatmap_max_combo(map)
    print(f"max_combo: {time.time() - st}")

    # Calculate pp
    pp_score, pp_if_fc = calculate_pp(score_ossapi, beatmap_max_combo, map)
    print(f"pp: {time.time() - st}")

    # Needs difficulty attribute for converted star ratings
    stars_converted = difficulty_attributes.attributes.star_rating
    st = time.time()
    # Correct Global rankings needs to be further calculated
    global_ranking = get_ranking_global(score_ossapi, oss)
    print(f"global_ranking: {time.time() - st}")

    st = time.time()
    # Initialize ScoreInfo
    score = ScoreInfo(
        score_ossapi=score_ossapi,
        count_geki=count_geki,
        stars_converted=stars_converted,
        count_katu=count_katu,
        pp=pp_score,
        pp_if_fc=pp_if_fc,
        beatmap_max_combo=beatmap_max_combo,
        global_ranking=global_ranking,
    )
    print(f"scoreInfo time: {time.time() - st}")
    print(f"total time: {time.time() - start_time}")
    return score
