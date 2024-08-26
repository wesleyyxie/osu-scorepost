from ossapi import Score


class ScoreInfo:
    """
    Represents score information needed for scorepost title and screenshot.
    """

    def __init__(
        self,
        score_ossapi=None,
        pp=None,
        pp_if_fc=None,
        count_katu=None,
        count_geki=None,
        beatmap_max_combo=None,
        stars_converted=None,
        global_ranking=None,
        username=None,
        id=None,
        best_id=None,
        beatmapset_artist=None,
        beatmapset_title=None,
        beatmap_version=None,
        beatmapset_creator=None,
        beatmap_id=None,
        beatmapset_id=None,
        mods=None,
        accuracy=None,
        mode=None,
        max_combo=None,
        score=None,
        beatmapset_status=None,
        count_300=None,
        count_100=None,
        count_50=None,
        count_miss=None,
        rank=None,
        created_at=None,
    ):
        """
        Initializes ScoreInfo with score details.

        Args:
            score_ossapi (Score): The score object from ossapi.
            pp (int): Performance points for the score.
            pp_if_fc (int): Performance points if full combo.
            katu (int | None): Number of katu.
            geki (int | None): Number of geki.
            beatmap_max_combo (int): Max combo possible on the beatmap.
            stars_converted (int): Converted star difficulty.
            global_ranking (int): Score's global ranking on the beatmap (0 if not in top 50).
        """
        if score_ossapi != None:
            self.username = score_ossapi._user.username
            self.id = score_ossapi.id
            self.best_id = score_ossapi.best_id
            self.beatmapset_artist = score_ossapi.beatmapset.artist
            self.beatmapset_title = score_ossapi.beatmapset.title
            self.beatmap_version = score_ossapi.beatmap.version
            self.beatmapset_creator = score_ossapi.beatmapset.creator
            self.beatmap_id = score_ossapi.beatmap.id
            self.beatmapset_id = score_ossapi.beatmapset.id
            self.mods = score_ossapi.mods.short_name()
            self.accuracy = score_ossapi.accuracy
            self.mode = score_ossapi.mode.value
            self.max_combo = score_ossapi.max_combo
            self.score = score_ossapi.score
            self.beatmapset_status = score_ossapi.beatmapset.status.value

            self.count_300 = score_ossapi.statistics.count_300
            self.count_100 = score_ossapi.statistics.count_100
            self.count_50 = score_ossapi.statistics.count_50
            self.count_miss = score_ossapi.statistics.count_miss
            self.rank = score_ossapi.rank.value
            self.created_at = (
                f'{score_ossapi.created_at.strftime("%d.%m.%Y %H:%M:%S")}.'
            )
        else:
            self.username = username
            self.id = id
            self.best_id = best_id
            self.beatmapset_artist = beatmapset_artist
            self.beatmapset_title = beatmapset_title
            self.beatmap_version = beatmap_version
            self.beatmapset_creator = beatmapset_creator
            self.beatmap_id = beatmap_id
            self.beatmapset_id = beatmapset_id
            self.mods = mods
            self.accuracy = accuracy
            self.mode = mode
            self.max_combo = max_combo
            self.score = score
            self.beatmapset_status = beatmapset_status

            self.count_300 = count_300
            self.count_100 = count_100
            self.count_50 = count_50
            self.count_miss = count_miss
            self.rank = rank
            self.created_at = created_at

        self.count_geki = count_geki
        self.count_katu = count_katu
        self.global_ranking = global_ranking

        self.pp = pp
        self.pp_if_fc = pp_if_fc

        self.beatmap_max_combo = beatmap_max_combo
        self.stars_converted = stars_converted
