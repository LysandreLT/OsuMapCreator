from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class SectionName(Enum):
    General = "[General]"
    Editor = "[Editor]"
    Metadata = "[Metadata]"
    Difficulty = "[Difficulty]"
    Events = "[Events]"
    TimingPoints = "[TimingPoints]"
    Colours = "[Colours]"
    HitObjects = "[HitObjects]"


@dataclass
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


@dataclass
class HitSample:
    normalSet: int = 0  # SampleSet
    additionSet: int = 0  # SampleSet
    index: int = 0
    volume: int = 0
    filename: Optional[str] = None

    def __str__(self):
        if self.filename is not None:
            return str(f"{self.normalSet}:{self.additionSet}:{self.index}:{self.volume}:{self.filename}:")
        else:
            return str(f"{self.normalSet}:{self.additionSet}:{self.index}:{self.volume}:")


@dataclass
class General(Section):
    AudioFilename: Optional[str] = None
    AudioLeadIn: int = 0
    AudioHash: Optional[str] = None  # deprecated
    PreviewTime: int = -1
    Countdown: int = 1
    SampleSet: str = "Normal"
    StackLeniency: float = 0.7
    Mode: int = 0
    LetterboxInBreaks: int = 0
    StoryFireInFront: int = 1  # deprecated
    UseSkinSprites: int = 0
    AlwaysShowPlayfield: int = 0  # deprecated
    OverlayPosition: str = "NoChange"
    SkinPreference: Optional[str] = None
    EpilepsyWarning: int = 0
    CountdownOffset: int = 0
    SpecialStyle: int = 0
    WidescreenStoryboard: int = 0
    SamplesMatchPlaybackRate: int = 0

    def parse_line(self, line: str):
        members = line.split(':')
        self.__setattr__(members[0], self.value(members[1]))


@dataclass
class Editor(Section):
    Bookmarks: Optional[List[int]] = None
    DistanceSpacing: float = 1.22
    BeatDivisor: int = 4
    GridSize: int = 4
    TimelineZoom: float = 1.0

    def parse_line(self, line: str):
        members = line.split(':')
        if members[0] == "Bookmarks":
            self.Bookmarks = [self.value(x) for x in members[1].split(",")]
        else:
            self.__setattr__(members[0], self.value(members[1]))


@dataclass
class Metadata(Section):
    Title: Optional[str] = None
    TitleUnicode: Optional[str] = None
    Artist: Optional[str] = None
    ArtistUnicode: Optional[str] = None
    Creator: Optional[str] = None
    Version: Optional[str] = None
    Source: Optional[str] = None
    Tags: Optional[List[str]] = None
    BeatmapID: int = 0
    BeatmapSetID: int = 0

    def parse_line(self, line: str):
        members = line.split(':')
        if members[0] == "Tags":
            self.Tags = [x for x in members[1].split(" ")]
        else:
            self.__setattr__(members[0], self.value(members[1]))


@dataclass
class Difficulty(Section):
    HPDrainRate: float = 5.0
    CircleSize: float = 5.0
    OverallDifficulty: float = 5.0
    ApproachRate: float = 5.0
    SliderMultiplier: float = 1.4
    SliderTickRate: float = 1.0

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


@dataclass
class TimingPoint(Section):
    time: int = 0
    beatLength: float = 0
    meter: int = 0
    sampleSet: int = 1  # SampleSet = SampleSet.Normal.value
    sampleIndex: int = 0
    volume: int = 1
    uninherited: int = 0
    effects: int = 0  # Effect = None

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

    def __str__(self):
        return f"{self.time},{self.beatLength},{self.meter},{self.sampleSet},{self.sampleIndex},{self.volume},{self.uninherited},{self.effects}"


class Colour:
    R: int
    G: int
    B: int


# TODO check wiki for colours
@dataclass
class ColourSection(Section):
    colours: List[Colour]
    slider_body: Colour
    slider_track_override: Colour
    slider_border: Colour

    # SliderTrackOverride
    # SliderBorder
    def parse_line(self, line):
        members = line.split(":")
        isCombo = line.startswith("Combo")
        split = members[1].split(",")
        if len(split) != 3 or len(split) != 4:
            print(" invalid color")
            return -1
        assert 0 <= split[0] <= 255
        assert 0 <= split[1] <= 255
        assert 0 <= split[2] <= 255

        if isCombo:
            # {"R": split[0], "G": split[1], "B": split[2]}
            self.colours.append(Colour(R=split[0], G=split[1], B=split[2]))
        else:
            # do nothing for the moment
            pass


@dataclass
class HitObject(Section):
    x: int = 0
    y: int = 0
    time: int = 0
    type: int = 0
    hitSound: int = 0
    hitSample: Optional[str] = HitSample().__str__()

    def __str__(self):
        return f"{self.x},{self.y},{self.time},{self.type},{self.hitSound},{self.hitSample}"

    def get_hit_sample(self, line) -> str:
        if self.has_hit_sample(line):
            return line
        return "0:0:0:0:0:"

    def has_hit_sample(self, line) -> bool:
        if type(line) == int or type(line) == float:
            return False
        else:
            return True


@dataclass
class Circle(HitObject):

    def parse_line(self, line):
        members = line.split(",")
        self.x = self.value(members[0])
        self.y = self.value(members[1])
        self.time = self.value(members[2])
        self.type = self.value(members[3])
        self.hitSound = self.value(members[4])
        self.hitSample = self.get_hit_sample(self.value(members[-1]))


@dataclass
class Spinner(HitObject):
    endTime: int = 0

    def parse_line(self, line):
        members = line.split(",")
        self.x = self.value(members[0])
        self.y = self.value(members[1])
        self.time = self.value(members[2])
        self.type = self.value(members[3])
        self.hitSound = self.value(members[4])
        self.endTime = self.value(members[5])

        self.hitSample = self.get_hit_sample(self.value(members[-1]))

    def __str__(self):
        return f"{self.x},{self.y},{self.time},{self.type},{self.hitSound},{self.endTime},{self.hitSample}"


@dataclass
class CurvePoint:
    x: int = 0
    y: int = 0

    def __str__(self):
        return f"{self.x}:{self.y}"


@dataclass
class Slider(HitObject):
    curvePoints: List[CurvePoint] = None
    slides: int = 0
    length: float = 0.0
    edgeSounds: str = ""
    edgeSets: str = ""
    curveType: str = ""

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
                self.curvePoints.append(curve_point)

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

    def __str__(self):
        curve_points = "|".join([cp.__str__() for cp in self.curvePoints])

        return f"{self.x},{self.y},{self.time},{self.type},{self.hitSound},{self.curveType}|{curve_points},{self.slides},{self.length},{self.edgeSounds},{self.edgeSets},{self.hitSample}"
