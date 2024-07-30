from .osu_api import *
import rosu_pp_py as rosu
import requests

# Creates title for osu
def create_title(url: str):
    
    # Score object from Ossapi
    score = get_score(url)

    username = score._user.username
    artist = score.beatmapset.artist
    title = score.beatmapset.title
    version = score.beatmap.version
    creator = score.beatmapset.creator

    fc = ""
    status = ""
    score_mode = ""
    
    # If score is set with NM, do not
    # display mods in title
    mods = ""
    if score.mods.value != 0:
        mods = f" +{score.mods}"

    # Difficulty attributes of score to get
    # converted star rating
    diff_attr = get_difficulty_attributes(score)
    stars_converted = diff_attr.attributes.star_rating

    # Accuracy
    if score.accuracy == 1:
        acc = "100%"
    else:
        acc = f"{score.accuracy * 100:.2f}%"

    # Mania players tend to display score number 
    # rounded to thousands
    if score.mode.value == "mania":
        score_amt = score.score // 1000
        acc = f"{score_amt}k {acc}"

    # Gamemode tags
    match score.mode.value:
        case "fruits":
            score_mode = "[osu!catch] "
        case "taiko":
            score_mode = "[osu!taiko] "
        case "mania":
            score_mode = "[osu!mania] "
        case "osu":
            score_mode = ""

    # Calculate pp of score with rosu-pp
    # Some statistics are set to None instead of 0 from the api
    number_50 = score.statistics.count_50 or 0
    number_100 = score.statistics.count_100 or 0
    number_misses = score.statistics.count_miss or 0
    number_katu = score.statistics.count_katu or 0
    number_300 = score.statistics.count_300 or 0
    number_geki = score.statistics.count_geki or 0

    perf_score = rosu.Performance(
        mods = score.mods.value,
        n100 = number_100,
        n50 = number_50,
        n300 = number_300,
        n_katu = number_katu,
        n_geki = number_geki,
        combo = score.max_combo,
        misses = number_misses,
    )

    response = requests.get(f"https://osu.ppy.sh/osu/{score.beatmap.id}")
    map = rosu.Beatmap(bytes = response.content)

    if score.mode.value == "fruits":
        map.convert(rosu.GameMode.Catch)
    elif score.mode.value == "taiko":
        map.convert(rosu.GameMode.Taiko)
    elif score.mode.value == "mania":
        map.convert(rosu.GameMode.Mania)
    elif score.mode.value == "osu":
        map.convert(rosu.GameMode.Osu)

    pp_score = round(perf_score.calculate(map).pp)
    performance_points = f"{pp_score}pp"

    # Beatmap status
    if score.beatmap.status.value != 1 and score.beatmap.status.value != 2:
        performance_points += " if ranked"
        status = score.beatmap.status.value
        match status:
            case 4:
                status = "LOVED "
            case 3:
                status = "QUALIFIED "
            case -2:
                status = "WIP "
    
    # If score is not an FC e.g. less than 20 combo from max beatmap combo
    # or if miss count is > 0
    if score.max_combo < score.beatmap.max_combo - 20 or score.statistics.count_miss > 0:

        # pp if FC (mania does not care about FC)
        if score.mode.value != "mania":
            perf_fc = rosu.Performance(
                mods = score.mods.value,
                n100 = number_100,
                n50 = number_50,
                n300 = number_300,
                n_katu = number_katu,
                n_geki = number_geki,
            )

            fc = f" {score.max_combo}/{score.beatmap.max_combo}x"
            if_fc_pp = round(perf_fc.calculate(map).pp)
            if score.statistics.count_miss > 0:
                fc += f" {score.statistics.count_miss}xMiss"
            elif score.mode.value == "osu":
                fc += " S-Rank"
            performance_points += f" ({if_fc_pp}pp if FC)"
    # If SS
    elif score.accuracy == 1:
        fc = " SS"
    else:
        fc = " FC"

    # Global ranking if on leaderboard
    if score.beatmap.status.value == 1 or score.beatmap.status.value == 3 or score.beatmap.status.value == 4 or score.beatmap.status.value == 2:
        rank_global = get_ranking_global(score)
        if rank_global != 0 and rank_global <= 50:
            fc += f" #{rank_global}"

    # Create title
    title = f"{score_mode}{username} | {artist} - {title} [{version}]{mods} ({creator}, {stars_converted:.2f}*) {acc}{fc} {status}| {performance_points}"
    return title

#print(create_title("https://osu.ppy.sh/scores/3241837339"))