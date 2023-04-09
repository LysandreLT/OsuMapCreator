from enum import Enum
from typing import List, Optional
import abc


class SectionName(Enum):
    General = "[General]",
    Editor = "[Editor]"
    Metadata = "[Metadata]"
    Difficulty = "[Difficulty]"
    Events = "[Events]"
    TimingPoints = "[TimingPoints]"
    Colours = "[Colours]"
    HitObjects = "[HitObjects]"


class Section:

    def value(self, value):
        if value.strip().isnumeric():
            return int(value)
        else:
            try:
                return float(value)
            except ValueError:
                return value

    def parse_line(self, line: str):
        ...


class HitSample:
    normalSet: int = 0  # SampleSet
    additionSet: int = 0  # SampleSet
    index: int = 0
    volume: int = 0
    filename: Optional[str]

    def set(self, normalSet: int, additionSet: int, index: int, volume: int, filename: Optional[str] = ""):
        self.normalSet = normalSet
        self.additionSet = additionSet
        self.index = index
        self.volume = volume
        self.filename = filename

    def __str__(self):
        if self.filename != "":
            return str(f"{self.normalSet}:{self.additionSet}:{self.index}:{self.volume}:{self.filename}:")
        else:
            return str(f"{self.normalSet}:{self.additionSet}:{self.index}:{self.volume}:")


class General(Section):
    AudioFilename: str = None
    AudioLeadIn: int = 0
    AudioHash: str = None
    PreviewTime: int = -1
    Countdown: int = 1
    SampleSet: str = "Normal"  # SampleSet.Normal.value
    StackLeniency: float = 0.7
    Mode: int = 0
    LetterboxInBreaks: int = 0
    StoryFireInFront: int = 1
    UseSkinSprites: int = 0
    AlwaysShowPlayfield: int = 0
    OverlayPosition: str = "NoChange"
    SkinPreference: str = None
    EpilepsyWarning: int = 0
    CountdownOffset: int = 0
    SpecialStyle: int = 0
    WidescreenStoryboard: int = 0
    SamplesMatchPlaybackRate: int = 0

    def parse_line(self, line: str):
        members = line.split(':')
        self.__setattr__(members[0], self.value(members[1]))


class Editor(Section):
    Bookmarks: List[int]
    DistanceSpacing: float = None
    BeatDivisor: int = None
    GridSize: int = None
    TimelineZoom: float = None

    def parse_line(self, line: str):
        members = line.split(':')
        if members[0] == "Bookmarks":
            self.Bookmarks = [self.value(x) for x in members[1].split(",")]
        else:
            self.__setattr__(members[0], self.value(members[1]))


class Metadata(Section):
    Title: str
    TitleUnicode: str
    Artist: str
    ArtistUnicode: str
    Creator: str
    Version: str
    Source: str
    Tags: List[str]
    BeatmapID: int
    BeatmapSetID: int

    def parse_line(self, line: str):
        members = line.split(':')
        if members[0] == "Tags":
            self.Tags = [x for x in members[1].split(" ")]
        else:
            self.__setattr__(members[0], self.value(members[1]))



class Difficulty(Section):
    HPDrainRate: float
    CircleSize: float
    OverallDifficulty: float
    ApproachRate: float
    SliderMultiplier: float
    SliderTickRate: float

    def parse_line(self, line: str):
        members = line.split(':')
        self.__setattr__(members[0], self.value(members[1]))

class EventParams:
    pass

class Event(Section):
    eventType: str
    startTime: int
    eventParams: List[EventParams]


class Background(EventParams):
    filename: str
    xOffset: int
    yOffset: int


class Video(EventParams):
    Video: 1
    startTime: int
    filename: str
    xOffset: int
    yOffset: int


class Pause(EventParams):
    # 2:Break TODO check wiki because sintaxe is strange
    Break: 2
    startTime: int
    endTime: int


#  TODO
class Storyboard(EventParams):
    pass


class TimingPoint(Section):
    time: int
    beatLength: float
    meter: int
    sampleSet: int = 1  # SampleSet = SampleSet.Normal.value
    sampleIndex: int = 0
    volume: int = 1
    uninherited: int
    effects: int = 0  # Effect = None
    bpm: int

    def parse_line(self, line: str):
        members = line.split(",")
        self.time = self.value(members[0])
        self.beatLength = self.value(members[1])
        self.meter = self.value(members[2])
        self.sampleSet = self.value(members[3])
        self.sampleIndex = self.value(members[4])
        self.volume = self.value(members[5])
        self.uninherited = self.value(members[6])
        self.effects = self.value(members[7])
        self.calculate_bpm()

    def calculate_bpm(self):
        self.bpm = round(60000 / self.beatLength)


# TODO check wiki for colours
class ColourObject(Section):
    Combo: int
    color: List[int]

    # SliderTrackOverride
    # SliderBorder
    def parse_line(self, line):
        pass


class HitObject(Section):
    x: int
    y: int
    time: int
    type: int = 0  # Type
    hitSound: int = 0
    hitSample: str  # Optional[HitSample]

    def get_hit_sample(self, line) -> str:
        if self.has_hit_sample(line):
            return line
        return "0:0:0:0:0:"

    def has_hit_sample(self, line) -> bool:
        if type(line) == int or type(line) == float:
            return False
        else:
            return True
    def get(self,_type):
        return self.__dict__.get(str(_type))

    def get_type(self, _type):
        if _type & 1:
            print("circle")
        elif _type & 2:
            print("slider")
        elif _type & 8:
            print("spinner")
        # elif _type & 128:
        #     print("mania")
        else:
            print("unknown type:", _type)

    def is_slider(self, _type) -> bool:
        if _type & 2:
            return True
        return False

    def is_spinner(self, _type) -> bool:
        if _type & 8:
            return True
        return False

    def is_circle(self, _type) -> bool:
        if _type & 1:
            return True
        return False


class Cercle(HitObject):
    def parse_line(self, line):
        members = line.split(",")
        self.x = self.value(members[0])
        self.y = self.value(members[1])
        self.time = self.value(members[2])
        self.type = self.value(members[3])
        self.hitSound = self.value(members[4])
        self.hitSample = self.get_hit_sample(self.value(members[-1]))




class Spinner(HitObject):
    endTime: int

    def parse_line(self, line):
        members = line.split(",")
        self.x = self.value(members[0])
        self.y = self.value(members[1])
        self.time = self.value(members[2])
        self.type = self.value(members[3])
        self.hitSound = self.value(members[4])
        self.endTime = self.value(members[5])

        self.hitSample = self.get_hit_sample(self.value(members[-1]))


class CurvePoint:
    x: int
    y: int

    def __str__(self):
        return f"{self.x}:{self.y}"


class Slider(HitObject):
    curveType: str
    curvePoints: List[CurvePoint]
    slides: int
    length: float
    edgeSounds: str
    edgeSets: str

    def parse_line(self, line):
        members = line.split(",")
        self.x = self.value(members[0])
        self.y = self.value(members[1])
        self.time = self.value(members[2])
        self.type = self.value(members[3])
        self.hitSound = self.value(members[4])

        # Parse slider points
        points = (members[5] or '').split('|')
        self.curveType = points[0]
        self.curvePoints = []
        if len(points):
            for i in range(1, len(points)):
                coordinates = points[i].split(':')
                curve_point = CurvePoint()
                curve_point.x = self.value(coordinates[0])
                curve_point.y = self.value(coordinates[1])
                # self.curvePoints.append(curve_point)
                self.curvePoints.append(curve_point.__str__())

        # Parse repeat slides bumber & length
        self.slides = int(members[6])
        self.length = int(round(float(members[7])))

        # Parse edgeSounds
        if len(members) > 9:
            if members[8]:
                self.edgeSounds = members[8]

            # Parse edgeSets
            if members[9]:
                self.edgeSets = members[9]

        self.hitSample = self.get_hit_sample(self.value(members[-1]))
