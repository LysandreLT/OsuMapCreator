from enum import Enum
from typing import List, Optional
import abc


class SectionName(Enum):
    General = "[General]"
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
    filename: Optional[str] = None

    def set(self, normalSet: int, additionSet: int, index: int, volume: int, filename: Optional[str] = ""):
        self.normalSet = normalSet
        self.additionSet = additionSet
        self.index = index
        self.volume = volume
        self.filename = filename

    def __str__(self):
        if self.filename is not None:
            return str(f"{self.normalSet}:{self.additionSet}:{self.index}:{self.volume}:{self.filename}:")
        else:
            return str(f"{self.normalSet}:{self.additionSet}:{self.index}:{self.volume}:")


class General(Section):

    def __init__(self,
                 AudioFilename: Optional[str] = None,
                 AudioLeadIn: Optional[int] = 0,
                 AudioHash: Optional[str] = None,
                 PreviewTime: Optional[int] = -1,
                 Countdown: Optional[int] = 1,
                 SampleSet: Optional[str] = "Normal",  # SampleSet.Normal.value
                 StackLeniency: Optional[float] = 0.7,
                 Mode: Optional[int] = 0,
                 LetterboxInBreaks: Optional[int] = 0,
                 StoryFireInFront: Optional[int] = 1,
                 UseSkinSprites: Optional[int] = 0,
                 AlwaysShowPlayfield: Optional[int] = 0,
                 OverlayPosition: Optional[str] = "NoChange",
                 SkinPreference: Optional[str] = None,
                 EpilepsyWarning: Optional[int] = 0,
                 CountdownOffset: Optional[int] = 0,
                 SpecialStyle: Optional[int] = 0,
                 WidescreenStoryboard: Optional[int] = 0,
                 SamplesMatchPlaybackRate: Optional[int] = 0):
        self.AudioFilename = AudioFilename
        self.OverlayPosition = OverlayPosition
        self.EpilepsyWarning = EpilepsyWarning
        self.SpecialStyle = SpecialStyle
        self.SamplesMatchPlaybackRate = SamplesMatchPlaybackRate
        self.WidescreenStoryboard = WidescreenStoryboard
        self.CountdownOffset = CountdownOffset
        self.SkinPreference = SkinPreference
        self.UseSkinSprites = UseSkinSprites
        self.AlwaysShowPlayfield = AlwaysShowPlayfield
        self.LetterboxInBreaks = LetterboxInBreaks
        self.StoryFireInFront = StoryFireInFront
        self.Mode = Mode
        self.StackLeniency = StackLeniency
        self.SampleSet = SampleSet
        self.Countdown = Countdown
        self.PreviewTime = PreviewTime
        self.AudioLeadIn = AudioLeadIn
        self.AudioHash = AudioHash

    def parse_line(self, line: str):
        members = line.split(':')
        self.__setattr__(members[0], self.value(members[1]))


class Editor(Section):
    def __init__(self,
                 Bookmarks: Optional[List[int]] = None,
                 DistanceSpacing: Optional[float] = None,
                 BeatDivisor: Optional[int] = None,
                 GridSize: Optional[int] = None,
                 TimelineZoom: Optional[float] = None):
        self.GridSize = GridSize
        self.BeatDivisor = BeatDivisor
        self.DistanceSpacing = DistanceSpacing
        self.Bookmarks = Bookmarks
        self.TimelineZoom = TimelineZoom

    def parse_line(self, line: str):
        members = line.split(':')
        if members[0] == "Bookmarks":
            self.Bookmarks = [self.value(x) for x in members[1].split(",")]
        else:
            self.__setattr__(members[0], self.value(members[1]))


class Metadata(Section):
    def __init__(self,
                 Title: Optional[str] = None,
                 TitleUnicode: Optional[str] = None,
                 Artist: Optional[str] = None,
                 ArtistUnicode: Optional[str] = None,
                 Creator: Optional[str] = None,
                 Version: Optional[str] = None,
                 Source: Optional[str] = None,
                 Tags: Optional[List[str]] = None,
                 BeatmapID: Optional[int] = None,
                 BeatmapSetID: Optional[int] = None):

        self.Tags = Tags
        self.BeatmapSetID = BeatmapSetID
        self.BeatmapID = BeatmapID
        self.Source = Source
        self.Version = Version
        self.Creator = Creator
        self.ArtistUnicode = ArtistUnicode
        self.Artist = Artist
        self.TitleUnicode = TitleUnicode
        self.Title = Title

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
    # x: int
    # y: int
    # time: int
    # type: int  # Type
    # hitSound: int = 0
    # hitSample: str  # Optional[HitSample]

    def __init__(self,
                 x: Optional[int] = 0,
                 y: Optional[int] = 0,
                 time: Optional[int] = 0,
                 type: Optional[int] = 0,  # Type
                 hitSound: Optional[int] = 0,
                 hitSample: Optional[str] = None):
        self.x = x
        self.y = y
        self.time = time
        self.type = type
        self.hitSound = hitSound
        if hitSample is None:
            self.hitSample = HitSample().__str__()
        else:
            self.hitSample = hitSample

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

    def get(self, _type):
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

    def __init__(self,
                 x: Optional[int] = 0,
                 y: Optional[int] = 0,
                 time: Optional[int] = 0,
                 type: Optional[int] = 0,  # Type
                 hitSound: Optional[int] = 0,
                 hitSample: Optional[str] = None):
        super().__init__(x, y, time, type, hitSound, hitSample)

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
