# create a beatmap set to give to the UI segment
import random
from typing import List, Optional

from MapCreator.Utils import utils
from MapCreator.Utils.models.models import General, Editor, Metadata, Difficulty, HitObject, SectionName, Cercle, Event, \
    TimingPoint


class BeatmapSet:
    def __init__(self):
        self.file_name = ""
        self.file_format = ""
        self.general: General = None
        self.editor: Editor = None
        self.metadata: Metadata = None
        self.difficulty: Difficulty = None
        self.events: Event = None
        self.timing_points = None
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

    def build_event(self, **kwargs):
        # one day maybe
        pass

    def build_timing_point(self, **kwargs):
        # one day maybe
        pass

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
        self.write_append(self.file_name, self.file_format)

        # general
        self.build_general(**{"AudioFilename": "audio.mp3"})
        resultList = [key + ":" + str(value) + "\n" for key, value in self.general.__dict__.items() if value != None]
        self.write_append(self.file_name, SectionName.General.value + "\n")
        self.write_append(self.file_name, resultList)

        # editor
        self.build_editor()
        resultList = [key + ":" + str(value) + "\n" for key, value in self.editor.__dict__.items() if value != None]
        self.write_append(self.file_name, "\n" + SectionName.Editor.value + "\n")
        self.write_append(self.file_name, resultList)

        # metadata
        self.build_metadata(
            **{"Title": "test", "TitleUnicode": "test", "Artist": "test", "ArtistUnicode": "test", "Creator": "test",
               "Version": "Normal"})
        resultList = [key + ":" + str(value) + "\n" for key, value in self.metadata.__dict__.items() if value != None]
        self.write_append(self.file_name, "\n" + SectionName.Metadata.value + "\n")
        self.write_append(self.file_name, resultList)

        # difficulty
        self.build_difficulty()
        resultList = [key + ":" + str(value) + "\n" for key, value in self.difficulty.__dict__.items() if value != None]
        self.write_append(self.file_name, "\n" + SectionName.Difficulty.value + "\n")
        self.write_append(self.file_name, resultList)

        # hit_object
        resultList = []
        for onset in onsets:
            hit_point = Cercle(
                **{"x": random.randrange(50, 500, 1), "y": random.randrange(50, 350, 1), "time": round(onset),
                   "type": 5,
                   "hitSound": random.randrange(0, 3, 1)}).__str__() + "\n"
            resultList.append(hit_point)

        self.write_append(self.file_name, "\n" + SectionName.HitObjects.value + "\n")
        self.write_append(self.file_name, resultList)

    def send_to_zip_test(self, name, path):
        utils.write_osz_archive(directory=path,
                                name=f"{path}/test-{name}")

    def write_append(self, file_name, lines):
        with open(file_name, 'a') as f:
            f.writelines(lines)

    def save_update(self):
        pass



if __name__ == "__main__":
    general = Editor()
    print(general.BeatDivisor)
