# test1 to cretae beatmap with just onset
import random
from typing import List

from MapCreator.Utils.beatmapset import BeatmapSet
from MapCreator.Utils.models.models import HitObject, Cercle
from MapCreator.Utils.utils import write_osz_archive
from MapCreator.music.music_analysis import compute_onset_superflux


def build_model(path, dest):
    onsets = compute_onset_superflux(path)
    beatmapset = BeatmapSet(dest)
    hit_points: List[HitObject] = []
    for onset in onsets:
        hit_point = Cercle(x=random.randrange(50, 600, 1), y=random.randrange(50, 400, 1), time=round(onset), type=5,
                           hitSound=random.randrange(0, 3, 1))
        hit_points.append(hit_point)

    beatmapset.build_beatmap_test()
    beatmapset.build_hit_points(hit_points)


if __name__ == "__main__":
    filepath = "C:/Users/hugob/dev/python/OsuMapCreator/MapCreator/datasets/maps/test/audio.mp3"
    dest = "C:/Users/hugob/dev/python/OsuMapCreator/MapCreator/datasets/maps/test/test.osu"
    build_model(filepath, dest)
    # write_osz_archive(directory="C:/Users/hugob/dev/python/OsuMapCreator/MapCreator/datasets/maps/test",
    #                   name="test_basic")

