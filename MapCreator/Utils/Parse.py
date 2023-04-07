import codecs
import os
import re
from bunch import bunchify

from Beatmap import Section, Structure, General, Editor


class Parse:
    def __init__(self):
        self.general = General()
        self.editor = Editor()
        self.structure = Structure()
        self.beatmap = {
            "file_format": "",
            f"{Section.General.name}": {},
            f"{Section.Editor.name}": {},
            f"{Section.Metadata.name}": {},
            f"{Section.Difficulty.name}": {},
            f"{Section.Events.name}": [],
            f"{Section.TimingPoints.name}": [],
            f"{Section.Colours.name}": [],
            f"{Section.HitObjects.name}": []
        }
        self.curve_types = {
            "C": "catmull",
            "B": "bezier",
            "L": "linear",
            "P": "pass-through"
        }

        self.osu_section = ""

        self.general_section = []
        self.editor_section = []
        self.metadata_section = []
        self.difficulty_section = []
        self.events_section = []
        self.timing_points_section = []
        self.colours_section = []
        self.hit_objects_section = []

        self.section_reg = re.compile('^\[([a-zA-Z0-9]+)\]$')
        self.key_val_reg = re.compile('^([a-zA-Z0-9]+)[ ]*:[ ]*(.+)$')

    def value(self, value: str):
        if value.isnumeric():
            return int(value)
        else:
            try:
                return float(value)
            except ValueError:
                return value

    def parse_general(self):
        general = {}
        for line in self.general_section:
            members = line.split(':')
            # for dict
            general[f"{members[0]}"] = self.value(members[1].strip())
            # for class
            if members[0] == "AudioFilename":
                self.general.AudioFilename = self.value(members[1].strip())
            elif members[0] == "AudioLeadIn":
                self.general.AudioLeadIn = self.value(members[1].strip())
            elif members[0] == "PreviewTime":
                self.general.PreviewTime = self.value(members[1].strip())
            elif members[0] == "Countdown":
                self.general.Countdown = self.value(members[1].strip())
            elif members[0] == "StackLeniency":
                self.general.StackLeniency = self.value(members[1].strip())
            elif members[0] == "Countdown":
                self.general.Countdown = self.value(members[1].strip())


        self.beatmap[f"{Section.General.name}"] = general


    def parse_editor(self):
        editor = {}
        for line in self.editor_section:
            members = line.split(':')
            editor[f"{members[0]}"] = self.value(members[1].strip())
        self.beatmap[f"{Section.Editor.name}"] = editor

    def parse_metadata(self):
        metadata = {}
        for line in self.metadata_section:
            members = line.split(':')
            metadata[f"{members[0]}"] = self.value(members[1].strip())
        self.beatmap[f"{Section.Metadata.name}"] = metadata
        if "Tags" in metadata:
            metadata["Tags"] = str(metadata["Tags"]).split(" ")

    def build_beatmap(self):
        self.parse_general()
        self.parse_editor()
        self.parse_metadata()

        self.structure.general = self.general
        self.structure.editor = self.editor

    def read_line(self, line: str):
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
                self.beatmap["file_format"] = line

    def parseFile(self, file):
        if os.path.isfile(file):
            with codecs.open(file, 'r', encoding="utf-8") as file:
                line = file.readline()
                while line:
                    self.read_line(line)
                    line = file.readline()


PATH = "C:/Users/hugob/dev/python/OsuMapCreator/MapCreator/app/ui/maps/1953850 RIOT - Overkill/RIOT - Overkill (Hareimu) [KILL THEM ALL].osu"


def read(path):
    with open(path) as f:
        content = f.readlines()
        # print(re.search(r"\[(.*?)\]",content).groupdict())
        for count, line in enumerate(content):
            match = re.search(r"\[(.*?)\]", line)
            if match:

                # print(match.group(1), "line : ", count + 1)
                if (match.group(1)) == (Section.Events.name):
                    print(match.string.strip(), "line : ", count + 1)




if __name__ == "__main__":
    parser = Parse()
    parser.parseFile(PATH)
    parser.build_beatmap()
    print(parser.structure.general.PreviewTime)
    # print(parser.beatmap[f"{Section.General.value}"])

    # general = General(**parser.beatmap[f"{Section.General.value}"])




    # read(PATH)

    # init parser
    # parser = osu.beatmapparser.BeatmapParser()
    #
    # # Parse File
    # time = datetime.datetime.now()
    # parser.parseFile(PATH)
    # print("Parsing done. Time: ", (datetime.datetime.now() - time).microseconds / 1000, 'ms')
    #
    # # Build Beatmap
    # time = datetime.datetime.now()
    # parser.build_beatmap()
    # print("Building done. Time: ", (datetime.datetime.now() - time).microseconds / 1000, 'ms')
    #
    # print(parser.beatmap, sep="\n")
