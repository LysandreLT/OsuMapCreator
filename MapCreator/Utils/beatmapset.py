# create a beatmap set to give to the UI segment
import random
from typing import List, Optional

from MapCreator.Utils import utils
from MapCreator.Utils.models.models import General, Editor, Metadata, Difficulty, HitObject, SectionName, Cercle, Event, \
    TimingPoint
from MapCreator.music.music_analysis import compute_change_in_bpm


class BeatmapSet:
    def __init__(self):
        self.file_name = ""
        self.file_format = ""
        self.general: General = None
        self.editor: Editor = None
        self.metadata: Metadata = None
        self.difficulty: Difficulty = None
        self.events: Event = None
        self.timing_points:List[TimingPoint] = []
        self.colours = None
        self.hit_objects: List[HitObject] = None

    def build_general(self, **kwargs):
        self.general = General(**kwargs)

    def build_editor(self, **kwargs):
        self.editor = Editor(**kwargs)

    def build_metadata(self, **kwargs):
        self.metadata = Metadata(**kwargs)

    def build_difficulty(self, **kwargs):
        self.difficulty = Difficulty(**kwargs)

    # [Events]
    # // Background and Video events
    # 0, 0, "yoiyoi2.jpg", 0, 0
    # // Break Periods
    # // Storyboard Layer 0(Background)
    # // Storyboard Layer 1(Fail)
    # // Storyboard Layer 2(Pass)
    # // Storyboard Layer 3(Foreground)
    # // Storyboard Layer 4(Overlay)
    # // Storyboard Sound Samples
    #
    # [TimingPoints]
    # 8692.70490823524, 428.571428571429, 4, 1, 0, 100, 1, 0 --> 60 * 1000 / 428.571 = 140 BPM --> 60 000 / BPM = beatLength

    def build_event(self, **kwargs):
        # one day maybe
        pass

    def build_timing_point(self, bpm, **kwargs):
        # one day maybe
        t = TimingPoint(**kwargs)
        t.calculate_beat_length(bpm)
        self.timing_points.append(t)

    def build_timing_points(self,path):
        # one day maybe
        beats = compute_change_in_bpm(path)
        for beat in beats:
            self.build_timing_point(beat[0], **{"time": beat[1],
                                                "beatLength": 0,
                                                "meter": 4,
                                                "sampleSet": 1,
                                                "sampleIndex": 0,
                                                "volume": 20,
                                                "uninherited": 1,
                                                "effects": 0})

    def build_colour(self, **kwargs):
        # one day maybe
        pass

    def build_hit_point(self, **kwargs):
        #     switch depending on the type of the hit object and pass all args
        pass

    def build_hit_points(self):
        pass

    def build_beatmap_test(self, onsets, dir_path, name):
        # for test purpose !!!
        # version
        self.file_name = f"{dir_path}/test-{name}.osu"
        self.file_format = "osu file format v14\n\n"
        self.write_append(self.file_name, self.file_format, 'w')

        # general
        self.build_general(**{"AudioFilename": "audio.mp3"})
        resultList = [key + ":" + str(value) + "\n" for key, value in self.general.__dict__.items() if value != None]
        self.write_append(self.file_name, SectionName.General.value + "\n", 'a')
        self.write_append(self.file_name, resultList, 'a')

        # editor
        self.build_editor()
        resultList = [key + ":" + str(value) + "\n" for key, value in self.editor.__dict__.items() if value != None]
        self.write_append(self.file_name, "\n" + SectionName.Editor.value + "\n", 'a')
        self.write_append(self.file_name, resultList, 'a')

        # metadata
        self.build_metadata(
            **{"Title": "test", "TitleUnicode": "test", "Artist": "test", "ArtistUnicode": "test", "Creator": "test",
               "Version": "Normal"})
        resultList = [key + ":" + str(value) + "\n" for key, value in self.metadata.__dict__.items() if value != None]
        self.write_append(self.file_name, "\n" + SectionName.Metadata.value + "\n", 'a')
        self.write_append(self.file_name, resultList, 'a')

        # difficulty
        self.build_difficulty()
        resultList = [key + ":" + str(value) + "\n" for key, value in self.difficulty.__dict__.items() if value != None]
        self.write_append(self.file_name, "\n" + SectionName.Difficulty.value + "\n", 'a')
        self.write_append(self.file_name, resultList, 'a')

        # timing points
        # self.build_timing_points(f"{dir_path}/audio.mp3")
        # resultList = [x.__str__() + "\n" for x in self.timing_points]
        # self.write_append(self.file_name, "\n" + SectionName.TimingPoints.value + "\n", 'a')
        # self.write_append(self.file_name, resultList, 'a')

        # hit_object
        resultList = []
        for onset in onsets:
            hit_point = Cercle(
                **{"x": random.randrange(50, 500, 1), "y": random.randrange(50, 350, 1), "time": round(onset),
                   "type": 5,
                   "hitSound": random.randrange(0, 3, 1)}).__str__() + "\n"
            resultList.append(hit_point)

        self.write_append(self.file_name, "\n" + SectionName.HitObjects.value + "\n", 'a')
        self.write_append(self.file_name, resultList, 'a')

    def send_to_zip_test(self, name, path):
        utils.write_osz_archive(directory=path,
                                name=f"{path}/test-{name}")

    def write_append(self, file_name, lines, mode):
        with open(file_name, mode) as f:
            f.writelines(lines)

    def save_update(self):
        pass


if __name__ == "__main__":
    general = Editor()
    print(general.BeatDivisor)
