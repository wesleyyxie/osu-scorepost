from ossapi import Ossapi, Score
from circleguard import Circleguard, ReplayMap
from circleguard.loader import NoInfoAvailableException
import rosu_pp_py as rosu
from requests import get
from os import getenv

from dotenv import find_dotenv, load_dotenv

# API information from .env
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
CLIENT_ID = getenv("CLIENT_ID")
CLIENT_SECRET = getenv("CLIENT_SECRET")
API_KEY = getenv("API_KEY")

from .score import ScoreInfo


def extract_id_from_link(input: str, oss: Ossapi):
    """Gets score id or user id from a link

    Args:
        input (str): The link without osu.ppy.sh/
        oss (Ossapi): Ossapi API instance

    Returns:
        Union[int, None]: The score ID or user ID as an integer if found, otherwise None.
    """

    # Splits the link into parts by /. If the link consists of
    # just a / at the end, then pop.
    # (e.g. https://osu.ppy.sh/scores/osu/2177560145/)
    link_parts = input.split("/")
    if link_parts[-1] == "":
        link_parts.pop()

    # Link should consist of 2 or 3 parts in order to be valid.
    # If unvalid, return None.
    if len(link_parts) == 2 or len(link_parts) == 3:
        # If it is a user link, try to convert the second part to
        # integer for the user id, otherwise assume the second
        # part is the username. If user method does not work,
        # return None.
        if link_parts[0] == "users":
            try:
                link_id = int(link_parts[1])
            except ValueError:
                try:
                    user = oss.user(link_parts[1])  # user object from Ossapi
                except ValueError:
                    return None
                link_id = user.id
        # If it is a score link, then it consists of 3 parts,
        # the id will be in the third position. If it consists
        # 2 parts, it will be in the second position. Then try
        # to make it an integer, otherwise return None.
        elif link_parts[0] == "scores":
            if len(link_parts) == 3:
                i = 2
            else:
                i = 1
            try:
                link_id = int(link_parts[i])
            except ValueError:
                return None
        return link_id
    else:
        return None


def get_recent_score(user_id: int, mode: str | None, oss: Ossapi):
    """Returns the most recent score from a user ID. If mode is None,
    return recent score from the default gamemode. Returns -1 if no
    recent scores found from a profile or None if the user_id is not valid.

    Args:
        user_id (int): The user ID
        mode (str | None): The gamemode
        oss (Ossapi): Ossapi API instance

    Returns:
        Union[Score, None, int]: The most recent score object, None if user_id
        is invalid, or -1 if the profile has no recent scores
    """

    # If mode is not None, try getting list of recent scores with mode specified,
    # else do not specify mode. If user_scores method does not return anything,
    # it will create a ValueError and function returns None.
    try:
        if mode != None:
            recent_scores = oss.user_scores(
                user_id=user_id,
                legacy_only=False,
                type="recent",
                mode=mode,
                limit=1,
                include_fails=True,
            )
        else:
            recent_scores = oss.user_scores(
                user_id=user_id,
                legacy_only=False,
                type="recent",
                limit=1,
                include_fails=True,
            )
    except ValueError:
        return None

    # If recent_scores is not empty, return the very first score.
    # Otherwise, there are no recent scores on the profile so return -1.
    if recent_scores != []:
        return recent_scores[0]
    else:
        return -1


def get_score_by_id(score_id: int, mode: str | None, oss: Ossapi):
    """Returns a score object found by the score_id. If score_id is
    invalid, return None. If mode is None, return recent score from
    the default gamemode.

    Args:
        score_id (int): Score ID
        mode (str | None): Gamemode
        oss (Ossapi): Ossapi API instance

    Returns:
        Union[Score, None]: Score object or None if score_id is invalid
    """

    # If mode is not None, try getting score with mode specified,
    # else do not specify mode. If score_mode or score method does not return anything,
    # it will create a ValueError and function returns None.
    try:
        if mode != None:
            score = oss.score_mode(mode, score_id)
        else:
            score = oss.score(score_id)
    except ValueError:
        return None
    return score


def get_ossapi_score(input: str, oss: Ossapi):
    """Processes an input from the user and returns a score object.
    If the input is a score link, return the corresponding score. If the
    input is a username or user link, return the user's most recent score
    including fails. Returns None if the the input is invalid, -1 if the
    user profile has no recent scores.

    Args:
        input (str): The user's input
        oss (Ossapi): Ossapi API instance

    Returns:
        Union[Score, -1, None]: Returns a score, None if the the input is
        invalid, or -1 if the user profile has no recent scores.
    """

    # If it is a link, shorten the input and extract the id from it.
    # If it is not a link then assume the input is a username and
    # try to get a user object by the username to get user id.
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
        except ValueError:
            return None
        link_id = user.id

    # If it is a user link or username, get the most recent score
    # by the link_id. If the gamemode is specified in the link, then
    # mode is the corresponding gamemode, else it is None.
    if "users/" in input or is_link == False:
        # If the input was just the username, then get recent score from default
        # gamemode
        if is_link == False:
            score = get_recent_score(link_id, None, oss)
        else:
            modes = {
                "/osu": "osu",
                "/taiko": "taiko",
                "/fruits": "fruits",
                "/mania": "mania",
            }
            mode = next((modes[i] for i in modes if i in input), None)
            score = get_recent_score(link_id, mode, oss)
    # If it is a score link, check if gamemode is specified. Else, mode is
    # just None
    else:
        modes = {
            "/osu/": "osu",
            "/taiko/": "taiko",
            "/fruits/": "fruits",
            "/mania/": "mania",
        }
        mode = next((modes[i] for i in modes if i in input), None)
        score = get_score_by_id(link_id, mode, oss)
    return score


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
                replay = ReplayMap(beatmap_id, user_id)
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


def calculate_pp(score_ossapi: Score, map: rosu.Beatmap):
    """Calculates the pp and pp if FC of a score

    Args:
        score_ossapi (Score): Score
        map (rosu.Beatmap): Beatmap data

    Returns:
        Tuple[int, int]: Tuple with pp of score, pp if FC
    """

    # Statistics of score is sometimes None
    number_50 = score_ossapi.statistics.count_50 or 0
    number_100 = score_ossapi.statistics.count_100 or 0
    number_misses = score_ossapi.statistics.count_miss or 0
    number_katu = score_ossapi.statistics.count_katu or 0
    number_300 = score_ossapi.statistics.count_300 or 0
    number_geki = score_ossapi.statistics.count_geki or 0

    # Calculate pp of score
    perf = rosu.Performance(
        mods=score_ossapi.mods.value,
        n100=number_100,
        n50=number_50,
        n300=number_300,
        n_katu=number_katu,
        n_geki=number_geki,
    )
    pp_if_fc = round(perf.calculate(map).pp)

    # Calculate pp of score if FC
    perf.set_misses(number_misses)
    perf.set_combo(score_ossapi.max_combo)
    pp = round(perf.calculate(map).pp)
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
    scores = oss.beatmap_scores(
        beatmap_id=score.beatmap.id, legacy_only=True, mode=score.mode.value
    )
    score_list = scores.scores

    # Calculate ranking by iterating through list of scores
    try:
        rank = next(i for i, s in enumerate(score_list, start=1) if s.id == score.id)
        return rank
    except StopIteration:
        # Returns 0 if score is not in leaderboard
        return 0


def get_score_info(input: str):
    """Returns score information needed for screenshot and scorepost title
    from a score link, username or user link

    Args:
        input (str): User input

    Returns:
        Union[Score_Info, int, None]: Returns Score_Info, None if input is invalid, or
        -1 if input was a user and there are no recent scores
    """

    # Initialize Ossapi and Circleguard API
    oss = Ossapi(CLIENT_ID, CLIENT_SECRET)
    cg = Circleguard(API_KEY)

    # Does not need to further process if score_ossapi
    # is -1 or None
    score_ossapi = get_ossapi_score(input, oss)
    if score_ossapi == -1:
        return -1
    elif score_ossapi == None:
        return None

    # Difficulty attributes for calculating converted star rating
    difficulty_attributes = oss.beatmap_attributes(
        beatmap_id=score_ossapi.beatmap.id,
        mods=score_ossapi.mods,
        ruleset=score_ossapi.mode.value,
    )

    # Geki and katu counts are only available for some scores that are
    # the user's best on the map
    geki, katu = count_geki_katu_osu(
        score_ossapi, score_ossapi.beatmap.id, score_ossapi.user_id, cg
    )

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

    # Calculate pp
    pp_score, pp_if_fc = calculate_pp(score_ossapi, map)

    # Limited beatmap information for recent scores so use rosu-pp
    # instead of Ossapi to get beatmap max combo
    beatmap_max_combo = get_beatmap_max_combo(map)

    # Needs difficulty attribute for converted star ratings
    stars_converted = difficulty_attributes.attributes.star_rating

    # Correct Global rankings needs to be further calculated
    global_ranking = get_ranking_global(score_ossapi, oss)

    # Initialize ScoreInfo
    score = ScoreInfo(
        score_ossapi=score_ossapi,
        geki=geki,
        stars_converted=stars_converted,
        katu=katu,
        pp=pp_score,
        pp_if_fc=pp_if_fc,
        beatmap_max_combo=beatmap_max_combo,
        global_ranking=global_ranking,
    )
    return score
