import codecs
import os
import re
from typing import List

from MapCreator.Utils.models.models import General, Editor, Metadata, Difficulty, Event, TimingPoint, ColourSection, \
    HitObject, SectionName, Slider, Spinner, Cercle


class Parser:
    def __init__(self):
        self.file_format = ""
        self.general = General()
        self.editor = Editor()
        self.metadata = Metadata()
        self.difficulty = Difficulty()
        self.events: List[Event] = []
        self.timing_points: List[TimingPoint] = []
        self.colours: List[ColourSection] = []
        self.hit_objects: List[HitObject] = []

        self.osu_section = ""

    def parse_hit_object_type(self, line):
        _type = int(line.split(",")[3].strip())
        # https://osu.ppy.sh/wiki/fr/Client/File_formats/Osu_%28file_format%29#type
        # convert in bit
        # 0: Cercle
        # 1: Slider
        # 3:Spinner
        # 7 osu mania
        if _type & 1:
            cercle = Cercle()
            cercle.parse_line(line)
            return cercle
        elif _type & 2:
            slider = Slider()
            slider.parse_line(line)
            return slider
        elif _type & 8:
            spinner = Spinner()
            spinner.parse_line(line)
            return spinner
        # elif _type & 128:
        #     print("mania")
        else:
            cercle = Cercle()
            cercle.parse_line(line)
            print("unknown type:", _type)
            return cercle

    def parse_line(self, line: str):
        line = line.strip()
        if not line:
            return

        match = re.search(r"\[(.*?)\]", line)
        if match:
            self.osu_section = match.group(0)
            return
        match = re.match('^osu file format (v[0-9]+)$', line)
        if match:
            # self.file_format = line
            self.file_format = match.group(1)
            return
        if self.osu_section == SectionName.General.value:
            self.general.parse_line(line)
        elif self.osu_section == SectionName.Editor.value:
            self.editor.parse_line(line)
        elif self.osu_section == SectionName.Metadata.value:
            self.metadata.parse_line(line)
        elif self.osu_section == SectionName.Difficulty.value:
            self.difficulty.parse_line(line)
        # elif self.osu_section == SectionName.Events.name:
        #     self.events_section.append(line)
        elif self.osu_section == SectionName.TimingPoints.value:
            timing_point = TimingPoint()
            timing_point.parse_line(line)
            self.timing_points.append(timing_point)
        # elif self.osu_section == SectionName.Colours.name:
        #     self.colours_section.append(line)
        elif self.osu_section == SectionName.HitObjects.value:
            hit_obj = self.parse_hit_object_type(line)
            self.hit_objects.append(hit_obj)

    def parse_file(self, file):
        if os.path.isfile(file):
            with codecs.open(file, 'r', encoding="utf-8") as file:
                line = file.readline()
                while line:
                    self.parse_line(line)
                    line = file.readline()


if __name__ == "__main__":

    PATH = "C:/Users/Lysandre/Documents/GitHub/OsuMapCreator/MapCreator/datasets/maps/67565 DragonForce - Valley of the " \
           "Damned/DragonForce - Valley of the Damned (Kayne) [Apocalypse].osu"
    parser = Parser()
    parser.parse_file(PATH)
    # print(parser.timing_points[0].time)
    print(parser.hit_objects)
    for o in parser.hit_objects:
        if isinstance(o, Cercle):
            print("true")
        else:
            print("false")
    # for obj in parser.hit_objects:
    #     # print(type(obj),obj.__dict__)
    #     print(obj.__dict__)
