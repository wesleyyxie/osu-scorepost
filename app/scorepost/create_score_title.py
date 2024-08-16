import os
import sys
#current_dir = os.path.dirname(os.path.abspath(__file__))
#sys.path.append(current_dir)
#print(sys.path)
from .util.get_score import get_score_info
from .util.score import ScoreInfo

# Creates title for osu
def create_title(score: ScoreInfo):
    if score == -1:
        return "No recent scores found"
    print("successfully got score")
    # Score object from Ossapi
    username = score.username
    artist = score.beatmapset_artist
    title = score.beatmapset_title
    version = score.beatmap_version
    creator = score.beatmapset_creator

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
    stars_converted = score.stars_converted

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

    performance_points = f"{score.pp}pp"

    # Beatmap status
    if score.beatmapset_status == 4 or score.beatmapset_status == 3 or score.beatmapset_status == -2:
        performance_points += " if ranked"
        status = score.beatmapset_status
        match status:
            case 4:
                status = "LOVED "
            case 3:
                status = "QUALIFIED "
            case -2:
                status = "WIP "
    
    if score.max_combo < score.beatmap_max_combo - 20 or score.count_miss > 0:
        # pp if FC (mania does not care about FC)
        if score.mode.value != "mania":
            fc = f" {score.max_combo}/{score.beatmap_max_combo}x"
            if_fc_pp = score.pp_if_fc
            if score.count_miss > 0:
                fc += f" {score.count_miss}xMiss"
            elif score.mode.value == "osu":
                fc += " S-Rank"
            if f"{score.rank}" == "F":
                fc += " FAIL"
            performance_points += f" ({if_fc_pp}pp if FC)"
    # If SS
    elif score.accuracy == 1:
        fc = " SS"
    else:
        fc = " FC"


    # Global ranking if on leaderboard
    if score.beatmapset_status == 1 or score.beatmapset_status == 3 or score.beatmapset_status == 4 or score.beatmapset_status == 2:
        rank_global = score.global_ranking
        if rank_global != 0 and rank_global <= 50:
            fc += f" #{rank_global}"

    # Create title

    title = f"{score_mode}{username} | {artist} - {title} [{version}]{mods} ({creator}, {stars_converted:.2f}*) {acc}{fc} {status}| {performance_points}"
    return title

#print(create_title("https://osu.ppy.sh/scores/329583391"))
#print(create_title("https://osu.ppy.sh/scores/328536"))
#print(create_title("https://osu.ppy.sh/users/11367222"))
#print(create_title("https://osu.ppy.sh/users/11367222/osu"))
#print(create_title(get_score_info("https://osu.ppy.sh/scores/3337662645")))
