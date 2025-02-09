import app.create_score_title as create_score_title
import app.util.get_score as get_score
import pytest


@pytest.mark.osu_ranked
@pytest.mark.parametrize(
    "score_link, expected_score_title",
    [
        (
            "https://osu.ppy.sh/scores/1649552691",
            "lily-an | xi - Ascension to Heaven [Death] +HDDTHR (Shiirn, 9.84*) 96.40% FC #6 | 1355pp",
        ),
        (
            "https://osu.ppy.sh/scores/1546684074",
            "Rupertion | Pratanallis - Braking Down [The Dawn that Breaks the Sorrowful Moonlight] +HDHR (Livermorium, 8.46*) 99.47% 2358/2378x 2xMiss #2 | 887pp (1003pp if FC)",
        ),
        (
            "https://osu.ppy.sh/scores/1715153265",
            "WhiteCat | Unlucky Morpheus - Angreifer [Scharfrichter] (Foxy Grandpa, 8.74*) 99.52% 2948/3490x S-Rank #2 | 988pp (1068pp if FC)",
        ),
        (
            "https://osu.ppy.sh/scores/osu/4459998279",
            "luvyouparadise | 55x55 - MY REZHEM KINOLENTY (feat. Cut The Crap) [CUT THE NORMAL] +DTHRFLSD (Shmiklak, 2.81*) 100% SS | 37pp",
        ),
        (
            "https://osu.ppy.sh/scores/osu/4459998278",
            "El Kami | S3RL - Bass Slut (Original Mix) [Reform's Filthy Expert] (Fatfan Kolek, 5.05*) 93.02% 268/492x 5xMiss | 79pp (114pp if FC)",
        ),
        (
            "https://osu.ppy.sh/scores/osu/4459998271",
            "Cartenpion | FELT - New World [Nightmare] (Hakurei Yoru, 6.55*) 91.74% 212/1358x 22xMiss | 107pp (267pp if FC)",
        ),
        (
            "https://osu.ppy.sh/scores/290372902",
            "Izzell_old | Pegboard Nerds - Try This [Collab Hard] +NF (Marmowka, 3.54*) 86.16% 75/457x 3xMiss | 15pp (27pp if FC)",
        ),
    ],
)
def test_osu_ranked(score_link: str, expected_score_title: str):
    score_info = get_score.get_score_info(score_link)
    score_title = create_score_title.create_title(score_info)
    if (
        score_info.global_ranking != 0
        and f"#{score_info.global_ranking}" not in expected_score_title
    ):
        rank = (expected_score_title.split(" #")[1]).split(" ")[0]
        expected_score_title = expected_score_title.replace(
            f"#{rank}", f"#{score_info.global_ranking}"
        )
    assert score_title == expected_score_title


@pytest.mark.osu_unranked
@pytest.mark.parametrize(
    "score_link, expected_score_title",
    [
        (
            "https://osu.ppy.sh/scores/981074188",
            "WhiteCat | Imagine Dragons - Warriors [1000lp challenger] +HR (Raikozen, 8.90*) 99.35% 915/918x 1xMiss #2 LOVED | 749pp if ranked (826pp if FC)",
        ),
        (
            "https://osu.ppy.sh/scores/1674443338",
            "WhiteCat | L.E.D.-G - BITTER CHOCOLATE STRIKER [CHALLENGE] (Raikozen, 8.67*) 99.77% FC #1 LOVED | 704pp if ranked",
        ),
        (
            "https://osu.ppy.sh/scores/osu/4100884541",
            "WhiteCat | Mrs. GREEN APPLE - Ao to Natsu (katagiri Bootleg) (Sped Up Ver.) [Summer] (apoq, 8.90*) 98.21% 1189/1466x 1xMiss #3 LOVED | 768pp if ranked (847pp if FC)",
        ),
        (
            "https://osu.ppy.sh/scores/4257457727",
            "MALISZEWSKI | Modern Talking - Last Exit To Brooklyn [Sytho's Trip to New York] +HD (-NeBu-, 8.20*) 99.93% FC #1 LOVED | 805pp if ranked",
        ),
        (
            "https://osu.ppy.sh/scores/4272187133",
            "nhutqui | Kurokotei - Nonbinarity [Insane] (Aerousea, 5.05*) 95.68% 879/1233x 1xMiss #15 LOVED | 100pp if ranked (115pp if FC)",
        ),
    ],
)
def test_osu_unranked(score_link, expected_score_title):
    score_info = get_score.get_score_info(score_link)
    score_title = create_score_title.create_title(score_info)
    if (
        score_info.global_ranking != 0
        and f"#{score_info.global_ranking}" not in expected_score_title
    ):
        rank = (expected_score_title.split(" #")[1]).split(" ")[0]
        expected_score_title = expected_score_title.replace(
            f"#{rank}", f"#{score_info.global_ranking}"
        )
    assert score_title == expected_score_title


@pytest.mark.taiko_ranked
@pytest.mark.parametrize(
    "score_link, expected_score_title",
    [
        (
            "https://osu.ppy.sh/scores/1878116373",
            "[osu!taiko] Peaceful | Halozy - Genryuu Kaiko [Higan Torrent] +HDDT (Axer, 8.33*) 99.82% FC #1 | 862pp",
        ),
        (
            "https://osu.ppy.sh/scores/taiko/124687458",
            "[osu!taiko] rendi508 | LAGOON - Kimi no Matsu Sekai (TV Size) [KwaN's Normal] +HR (HabiHolic, 1.92*) 97.41% FC | 48pp",
        ),
        (
            "https://osu.ppy.sh/scores/4315142893",
            "[osu!taiko] la1yk | Shizuru (CV: Nabatame Hitomi), Rino (CV: Asumi Kana) - SUPER CHOCOLATE (Game Ver.) [TYIS' KANTAN] ([-E S I A-], 1.54*) 90.60% 129/133x 4xMiss #31 | 25pp (28pp if FC)",
        ),
    ],
)
def test_taiko_ranked(score_link, expected_score_title):
    score_info = get_score.get_score_info(score_link)
    score_title = create_score_title.create_title(score_info)
    if (
        score_info.global_ranking != 0
        and f"#{score_info.global_ranking}" not in expected_score_title
    ):
        rank = (expected_score_title.split(" #")[1]).split(" ")[0]
        expected_score_title = expected_score_title.replace(
            f"#{rank}", f"#{score_info.global_ranking}"
        )
    assert score_title == expected_score_title


@pytest.mark.taiko_unranked
@pytest.mark.parametrize(
    "score_link, expected_score_title",
    [
        (
            "https://osu.ppy.sh/scores/1877420225",
            "[osu!taiko] Peaceful | Fleshgod Apocalypse - The Deceit / The Violation [Raiden's Terror Oni] +HD (Mazzerin, 8.14*) 99.66% FC #1 LOVED | 740pp if ranked",
        ),
        (
            "https://osu.ppy.sh/scores/4287363054",
            "[osu!taiko] Spicy Onion | katagiri - Magical Girl Tour 2019 [YAZD feat.apple] (Ozu, 8.37*) 92.99% 555/2127x 62xMiss #12 LOVED | 247pp if ranked (539pp if FC)",
        ),
    ],
)
def test_taiko_unranked(score_link, expected_score_title):
    score_info = get_score.get_score_info(score_link)
    score_title = create_score_title.create_title(score_info)
    if (
        score_info.global_ranking != 0
        and f"#{score_info.global_ranking}" not in expected_score_title
    ):
        rank = (expected_score_title.split(" #")[1]).split(" ")[0]
        expected_score_title = expected_score_title.replace(
            f"#{rank}", f"#{score_info.global_ranking}"
        )
    assert score_title == expected_score_title


# Mania scores get Lazer accuracy for some reason
@pytest.mark.mania_ranked
@pytest.mark.parametrize(
    "score_link, expected_score_title",
    [
        (
            "https://osu.ppy.sh/scores/2344387027",
            "[osu!mania] dressurf | Xyris - Eviternity [[7K] Transcend Light] (Critical_Star, 10.93*) 966k 99.03% #1 | 1482pp",
        ),
        (
            "https://osu.ppy.sh/scores/2344457961",
            "[osu!mania] dressurf | HyuN feat. Sennzai - Duplicity Shade [[7K] Metamorphosis] (_underjoy, 11.39*) 961k 98.83% #1 | 1604pp",
        ),
        (
            "https://osu.ppy.sh/scores/2833622439",
            "[osu!mania] dressurf | Laur - Laur-chan Taisou Daiichi [[7K] Finger Choreography] +PF (Carpihat, 5.93*) 997k 99.88% FC #1 | 408pp",
        ),
        (
            "https://osu.ppy.sh/scores/mania/184689664",
            "[osu!mania] -[Aquarius]- | RAMM ni Haiyoru Tamao-san - Kirai na WaKe Lychee [victorica's 4K Lv.12] (Lieselotte, 3.48*) 517k 81.98% | 0pp",
        ),
        (
            "https://osu.ppy.sh/scores/mania/412112112",
            "[osu!mania] Celorig | RAN - Dekat di Hati (REDSHiFT Remix) [[4K] Maximum] +DT ([ A v a l o n ], 4.68*) 807k 94.65% | 149pp",
        ),
    ],
)
def test_mania_ranked(score_link, expected_score_title):
    score_info = get_score.get_score_info(score_link)
    score_title = create_score_title.create_title(score_info)
    if (
        score_info.global_ranking != 0
        and f"#{score_info.global_ranking}" not in expected_score_title
    ):
        rank = (expected_score_title.split(" #")[1]).split(" ")[0]
        expected_score_title = expected_score_title.replace(
            f"#{rank}", f"#{score_info.global_ranking}"
        )
    assert score_title == expected_score_title


@pytest.mark.mania_unranked
@pytest.mark.parametrize(
    "score_link, expected_score_title",
    [
        (
            "https://osu.ppy.sh/scores/3130393304",
            "[osu!mania] Kalkai | GFRIEND - Time for the moon night [[7K] ByeolBit] (Jinjin, 7.86*) 989k 99.45% #3 LOVED | 715pp if ranked",
        ),
        (
            "https://osu.ppy.sh/scores/4311144256",
            "[osu!mania] PocaFanboy | DJ TOTTO - DORNWALD ~Junge~ [[4K] Anima] (stupud man, 4.11*) 999k 99.95% #1 LOVED | 179pp if ranked",
        ),
    ],
)
def test_mania_unranked(score_link, expected_score_title):
    score_info = get_score.get_score_info(score_link)
    score_title = create_score_title.create_title(score_info)
    if (
        score_info.global_ranking != 0
        and f"#{score_info.global_ranking}" not in expected_score_title
    ):
        rank = (expected_score_title.split(" #")[1]).split(" ")[0]
        expected_score_title = expected_score_title.replace(
            f"#{rank}", f"#{score_info.global_ranking}"
        )
    assert score_title == expected_score_title


@pytest.mark.catch_ranked
@pytest.mark.parametrize(
    "score_link, expected_score_title",
    [
        (
            "https://osu.ppy.sh/scores/3021430401",
            "[osu!catch] Motion | MY FIRST STORY - REVIVER [RESURRECTION] +HDDT (Secre, 9.21*) 99.69% FC #4 | 1310pp",
        ),
        (
            "https://osu.ppy.sh/scores/2327036403",
            "[osu!catch] Motion | Noah - Deadly force - Put an end [Revolt from the Abyss] +HDHR (Bunnrei, 10.34*) 99.97% 3116/3333x 1xMiss #5 | 1543pp (1681pp if FC)",
        ),
        (
            "https://osu.ppy.sh/scores/fruits/184689664",
            "[osu!catch] -[CocoaFangirl] | ASCA - RESISTER (TV Size) [SMOKELIND's INSANE] +HD (Sotarks, 3.67*) 100% SS #10 | 160pp",
        ),
        (
            "https://osu.ppy.sh/scores/fruits/154689664",
            "[osu!catch] Sokolov42 | Aoi Eir - Sirius (TV size ver.) [Hard] (deetz, 1.98*) 99.18% 420/423x 1xMiss | 38pp (41pp if FC)",
        ),
    ],
)
def test_catch_ranked(score_link, expected_score_title):
    score_info = get_score.get_score_info(score_link)
    score_title = create_score_title.create_title(score_info)
    if (
        score_info.global_ranking != 0
        and f"#{score_info.global_ranking}" not in expected_score_title
    ):
        rank = (expected_score_title.split(" #")[1]).split(" ")[0]
        expected_score_title = expected_score_title.replace(
            f"#{rank}", f"#{score_info.global_ranking}"
        )
    assert score_title == expected_score_title


@pytest.mark.catch_unranked
@pytest.mark.parametrize(
    "score_link, expected_score_title",
    [
        (
            "https://osu.ppy.sh/scores/1958028585",
            "[osu!catch] ExGon | eFeL - Broken Hearts [Hope] +FL (ExGon, 10.74*) 100% SS #1 LOVED | 1937pp if ranked",
        ),
        (
            "https://osu.ppy.sh/scores/1935457997",
            "[osu!catch] God Gosu | DJ Noriken - #The_Relentless_(Modified) [EX] (CLSW, 6.15*) 99.14% 1821/2553x 21xMiss #27 LOVED | 202pp if ranked (522pp if FC)",
        ),
    ],
)
def test_catch_unranked(score_link, expected_score_title):
    score_info = get_score.get_score_info(score_link)
    score_title = create_score_title.create_title(score_info)
    if (
        score_info.global_ranking != 0
        and f"#{score_info.global_ranking}" not in expected_score_title
    ):
        rank = (expected_score_title.split(" #")[1]).split(" ")[0]
        expected_score_title = expected_score_title.replace(
            f"#{rank}", f"#{score_info.global_ranking}"
        )
    assert score_title == expected_score_title
