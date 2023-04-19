import librosa

from MapCreator.Utils.beatmapset import BeatmapSet
from MapCreator.music import music_analysis
from MapCreator.music.music_analysis import compute_local_bpm, compute_change_in_bpm


# creation of beatmap based on the onset from peak to peak detection / beatrate, plp and other similar methods
def build_model_superflux(audio_path, dir_path):
    onsets = music_analysis.compute_onset_superflux(audio_path)
    beatmapset = BeatmapSet()
    beatmapset.build_beatmap_test(onsets, dir_path, "superflux")
    beatmapset.send_to_zip_test("superflux", dir_path)


def build_model_default(audio_path, dir_path):
    onsets = music_analysis.compute_onset_default(audio_path)
    beatmapset = BeatmapSet()
    beatmapset.build_beatmap_test(onsets, dir_path, "default")
    beatmapset.send_to_zip_test("default", dir_path)


def build_model_plp(audio_path, dir_path):
    onsets = music_analysis.compute_plp(audio_path)
    beatmapset = BeatmapSet()
    beatmapset.build_beatmap_test(onsets, dir_path, "plp")
    beatmapset.send_to_zip_test("plp", dir_path)


def build_model_plp_log(audio_path, dir_path):
    onsets = music_analysis.compute_plp_prior(audio_path)
    beatmapset = BeatmapSet()
    beatmapset.build_beatmap_test(onsets, dir_path, "plp-log")
    beatmapset.send_to_zip_test("plp-log", dir_path)


def build_model_beat(audio_path, dir_path):
    onsets = music_analysis.compute_beat_track(audio_path)
    beatmapset = BeatmapSet()
    beatmapset.build_beatmap_test(onsets, dir_path, "beat")
    beatmapset.send_to_zip_test("beat", dir_path)


def test_timing_points(audio_path, dir_path):
    # onsets = music_analysis.compute_plp(audio_path)
    # print(onsets)
    beats = compute_change_in_bpm(audio_path)


def test_correction_time(audio_path, dir_path):
    pass


if __name__ == "__main__":
    filepath = "C:/Users/hugob/dev/python/OsuMapCreator/MapCreator/datasets/maps/test/audio.mp3"
    dir_path = "C:/Users/hugob/dev/python/OsuMapCreator/MapCreator/datasets/maps/test"
    # build_model_superflux(filepath,dir_path)
    # build_model_default(filepath,dir_path)
    # build_model_plp(filepath,dir_path)
    # build_model_plp_log(filepath,dir_path)
    # build_model_beat(filepath,dir_path)
    test_timing_points(filepath, dir_path)
    test_correction_time(filepath, dir_path)
