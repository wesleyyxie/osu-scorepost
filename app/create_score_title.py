from util.score import ScoreInfo
import time


def create_title(score: ScoreInfo):
    """Returns the title of the scorepost

    Args:
        score (ScoreInfo): _description_

    Returns:
        str: Title
    """
    # Initialize information
    username = score.username
    artist = score.beatmapset_artist
    title = score.beatmapset_title
    version = score.beatmap_version
    creator = score.beatmapset_creator

    # If score is set with NM, do not
    # display mods in title
    if score.mods != "NM":
        mods = f" +{score.mods}"
    else:
        mods = ""

    # Difficulty attributes of score to get
    # converted star rating
    stars_converted = score.stars_converted

    # Accuracy
    if score.accuracy == 1:
        acc = "100%"
    else:
        acc = f"{score.accuracy * 100:.2f}%"

    # Mania players tend to display score number
    # rounded to thousands
    if score.mode == "mania":
        score_amt = score.score // 1000
        acc = f"{score_amt}k {acc}"

    # Gamemode tags
    score_mode = {
        "fruits": "[osu!catch] ",
        "taiko": "[osu!taiko] ",
        "mania": "[osu!mania] ",
        "osu": "",
    }.get(score.mode, "")

    performance_points = f"{score.pp}pp"
    if score.beatmapset_status == 1 and score.id != score.best_id and score.rank != "F":
        performance_points += " if submitted"
    # Beatmap status
    if score.beatmapset_status != 1 and score.beatmapset_status != 2:
        performance_points += " if ranked"
        status = {4: "LOVED ", 3: "QUALIFIED ", -1: "WIP ", -2: " ", 0: " "}.get(
            score.beatmapset_status
        )
    else:
        status = ""

    # If score is not FC (score combo is 20 less than max combo or count miss > 0)
    fc = ""
    if score.max_combo < score.beatmap_max_combo - 20 or score.count_miss > 0:
        # pp if FC (mania does not care about FC)
        if score.mode != "mania":
            fc = f" {score.max_combo}/{score.beatmap_max_combo}x"
            if_fc_pp = score.pp_if_fc
            if score.count_miss > 0:
                fc += f" {score.count_miss}xMiss"
            elif score.mode == "osu" and (
                f"{score.rank}" == "S" or f"{score.rank}" == "SH"
            ):
                fc += " S-Rank"
            performance_points += f" ({if_fc_pp}pp if FC)"
    # If SS
    elif score.accuracy == 1:
        fc = " SS"
    else:
        fc = " FC"

    if f"{score.rank}" == "F":
        fc += " FAIL"

    # Global ranking if in top 50
    if (
        score.beatmapset_status == 1
        or score.beatmapset_status == 3
        or score.beatmapset_status == 4
        or score.beatmapset_status == 2
    ):
        rank_global = score.global_ranking
        if rank_global != 0 and rank_global <= 50:
            fc += f" #{rank_global}"

    # Create title
    title = f"{score_mode}{username} | {artist} - {title} [{version}]{mods} ({creator}, {stars_converted:.2f}*) {acc}{fc} {status}| {performance_points}"
    return title
