from ossapi import Score

class ScoreInfo:
    def __init__(self, score_ossapi: Score, pp: int, pp_if_fc: int, katu: int, geki: int, beatmap_max_combo: int, stars_converted: int, global_ranking: int):
        self.username = score_ossapi._user.username
        self.id = score_ossapi.id
        self.best_id = score_ossapi.best_id
        self.beatmapset_artist = score_ossapi.beatmapset.artist
        self.beatmapset_title = score_ossapi.beatmapset.title
        self.beatmap_version = score_ossapi.beatmap.version
        self.beatmapset_creator = score_ossapi.beatmapset.creator
        self.beatmap_id = score_ossapi.beatmap.id
        self.beatmapset_id = score_ossapi.beatmapset.id
        self.mods = score_ossapi.mods
        self.accuracy = score_ossapi.accuracy
        self.mode = score_ossapi.mode
        self.max_combo = score_ossapi.max_combo
        self.score = score_ossapi.score
        self.beatmapset_status = score_ossapi.beatmapset.status.value

        self.count_300 = score_ossapi.statistics.count_300
        self.count_100 = score_ossapi.statistics.count_100
        self.count_50 = score_ossapi.statistics.count_50
        self.count_geki = geki
        self.count_katu = katu
        self.count_miss = score_ossapi.statistics.count_miss
        self.rank = score_ossapi.rank.value
        self.created_at = score_ossapi.created_at
        self.global_ranking = global_ranking

        self.pp = pp
        self.pp_if_fc = pp_if_fc

        self.beatmap_max_combo = beatmap_max_combo
        self.stars_converted = stars_converted
    

        


    
        