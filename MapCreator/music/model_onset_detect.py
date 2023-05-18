from MapCreator.Utils.beatmapset import BeatmapSet
from MapCreator.music import music_analysis

# creation of beatmap based on the onset from peak to peak detection / beatrate, plp and other similar methods
def build_model_superflux(path):
    onsets = music_analysis.compute_onset_superflux(path)
    beatmapset = BeatmapSet()
    beatmapset.build_beatmap_test(onsets,"superflux")
    beatmapset.send_to_zip_test("superflux")

def build_model_default(path):
    onsets = music_analysis.compute_onset_default(path)
    beatmapset = BeatmapSet()
    beatmapset.build_beatmap_test(onsets,"default")
    beatmapset.send_to_zip_test("default")

def build_model_plp(path):
    onsets = music_analysis.compute_plp(path)
    beatmapset = BeatmapSet()
    beatmapset.build_beatmap_test(onsets,"plp")
    beatmapset.send_to_zip_test("plp")

def build_model_plp_log(path):
    onsets = music_analysis.compute_plp_prior(path)
    beatmapset = BeatmapSet()
    beatmapset.build_beatmap_test(onsets,"plp-log")
    beatmapset.send_to_zip_test("plp-log")

def build_model_beat(path):
    onsets = music_analysis.compute_beat_track(path)
    beatmapset = BeatmapSet()
    beatmapset.build_beatmap_test(onsets,"beat")
    beatmapset.send_to_zip_test("beat")

if __name__ == "__main__":
    filepath = "C:/Users/hugob/dev/python/OsuMapCreator/MapCreator/datasets/maps/test/audio.mp3"
    build_model_superflux(filepath)
    build_model_default(filepath)
    # build_model_plp(filepath)
    # build_model_plp_log(filepath)
    # build_model_beat(filepath)




