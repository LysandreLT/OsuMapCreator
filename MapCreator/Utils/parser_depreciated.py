import codecs
import inspect
import os
import re
from typing import List
import osuparser

from models_depreciated import Section, Structure, General, Editor, Metadata, Difficulty, TimingPoint, Event, ColourObject, \
    HitObject, HitSample, Spinner, Slider


class Parse:
    def __init__(self):
        self.structure = Structure()
        self.general = General()
        self.editor = Editor()
        self.metadata = Metadata()
        self.difficulty = Difficulty()
        self.events:List[Event] = []
        self.timing_points: List[TimingPoint] = []
        self.colours: List[ColourObject] = []
        self.hit_objects:List[HitObject] = []

        self.osu_section = ""

        self.general_section = []
        self.editor_section = []
        self.metadata_section = []
        self.difficulty_section = []
        self.events_section = []
        self.timing_points_section = []
        self.colours_section = []
        self.hit_objects_section = []

    def value(self, value: str):
        if value.strip().isnumeric():
            return int(value)
        else:
            try:
                return float(value)
            except ValueError:
                return value


    def map_to_class_attribute(self, members: str, type_):
        for i in inspect.getmembers(type_):
            if not i[0].startswith('_'):
                if not inspect.ismethod(i[1]):
                    key, value = i
                    if key == members[0]:
                        type_.__setattr__(key, self.value(members[1]))
                        # print("key:", key, " / value:", attribute.__getattribute__(key))

    def parse_general(self):
        for line in self.general_section:
            members = line.split(':')
            self.map_to_class_attribute(members, self.general)

    def parse_editor(self):
        for line in self.editor_section:
            members = line.split(':')
            self.map_to_class_attribute(members, self.editor)
            if members[0] == "Bookmarks":
                self.editor.Bookmarks = [self.value(x) for x in members[1].split(",")]



    def parse_metadata(self):
        for line in self.metadata_section:
            members = line.split(':')
            self.map_to_class_attribute(members, self.metadata)
            if members[0] == "Tags":
                self.metadata.Tags = [x for x in members[1].split(" ")]

    def parse_difficulty(self):
        for line in self.difficulty_section:
            members = line.split(":")
            self.map_to_class_attribute(members, self.difficulty)

    def parse_events(self):
        pass

    def parse_timing_points(self):
        for line in self.timing_points_section:
            members = line.split(",")
            timing_point = TimingPoint()
            timing_point.time = self.value(members[0])
            timing_point.beatLength = self.value(members[1])
            timing_point.meter = self.value(members[2])
            timing_point.sampleSet = self.value(members[3])
            timing_point.sampleIndex = self.value(members[4])
            timing_point.volume = self.value(members[5])
            timing_point.uninherited = self.value(members[6])
            timing_point.effects = self.value(members[7])
            self.timing_points.append(timing_point)

    def parse_colours(self):
        pass

    def parse_hit_sample(self,hit_sample_members : str) -> HitSample:
        members = hit_sample_members.split(":")
        hit_sample = HitSample()
        hit_sample.normalSet = self.value(members[0])
        hit_sample.additionSet = self.value(members[1])
        hit_sample.index = self.value(members[2])
        hit_sample.volume = self.value(members[3])

        hit_sample.filename = members[4]

    def parse_obj_params(self,params:str,_type):
        if params:
            print(params)
            if _type & 1:
                slider = Slider()
                print("slider",params)
                return slider
            elif _type & 3:
                spinner = Spinner()
                spinner.endTime = params
                return spinner
            elif _type & 7:
                print("mania")
            else:
                print("unknown type:",_type)

    def parse_hit_objects(self):

        for line in self.hit_objects_section:
            members = line.split(",")
            hit_object = HitObject()
            hit_object.x = self.value(members[0])
            hit_object.y = self.value(members[1])
            hit_object.time = self.value(members[2])
            hit_object.type = self.value(members[3])
            hit_object.hitSound = self.value(members[4])

            # if > 1 means there is hitSample -> if type 1 or 3, param = members[5:-1]
            # else no hitSample and if type 1 or 3, param = members[5:]
            if len(members[-1].split(":")) > 1:
                hit_object.hitSample = self.parse_hit_sample(members[-1])
                # print(members[-1].split(":"))
                self.parse_obj_params(members[5:-1],hit_object.type)
            else:
                hit_object.hitSample = HitSample().set(0,0,0,0)
                self.parse_obj_params(members[5:], hit_object.type)

            self.hit_objects.append(hit_object)

    def build_beatmap(self):
        self.structure = Structure()
        self.parse_editor()
        self.parse_metadata()
        self.parse_difficulty()
        self.parse_events()
        self.parse_timing_points()
        self.parse_colours()
        self.parse_hit_objects()

        self.structure.general = self.general
        self.structure.editor = self.editor
        self.structure.metadata = self.metadata
        self.structure.difficulty = self.difficulty
        self.structure.events = self.events
        self.structure.timing_points = self.timing_points
        self.structure.colours = self.colours

    def parse_line(self, line: str):
        line = line.strip()
        if not line:
            return

        match = re.search(r"\[(.*?)\]", line)
        if match:
            self.osu_section = match.group(1)
            return

        if self.osu_section == Section.General.name:
            self.general_section.append(line)
        elif self.osu_section == Section.Editor.name:
            self.editor_section.append(line)
        elif self.osu_section == Section.Metadata.name:
            self.metadata_section.append(line)
        elif self.osu_section == Section.Difficulty.name:
            self.difficulty_section.append(line)
        elif self.osu_section == Section.Events.name:
            self.events_section.append(line)
        elif self.osu_section == Section.TimingPoints.name:
            self.timing_points_section.append(line)
        elif self.osu_section == Section.Colours.name:
            self.colours_section.append(line)
        elif self.osu_section == Section.HitObjects.name:
            self.hit_objects_section.append(line)

        else:
            match = re.match('^osu file format (v[0-9]+)$', line)
            if match:
                self.structure.file_format = line

    def parseFile(self, file):
        if os.path.isfile(file):
            with codecs.open(file, 'r', encoding="utf-8") as file:
                line = file.readline()
                while line:
                    self.parse_line(line)
                    line = file.readline()



PATH = "C:/Users/hugob/dev/python/OsuMapCreator/MapCreator/app/ui/maps/1953850 RIOT - Overkill/RIOT - Overkill (Hareimu) [KILL THEM ALL].osu"

if __name__ == "__main__":
    parser = Parse()
    parser.parseFile(PATH)
    parser.build_beatmap()
    # print(parser.hit_objects[0].type)

