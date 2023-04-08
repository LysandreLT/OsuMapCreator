from enum import Enum
from typing import List, Optional


class Section(Enum):
    General = "[General]",
    Editor = "[Editor]"
    Metadata = "[Metadata]"
    Difficulty = "[Difficulty]"
    Events = "[Events]"
    TimingPoints = "[TimingPoints]"
    Colours = "[Colours]"
    HitObjects = "[HitObjects]"


class Effect(Enum):
    KiaiTime: int(0)
    OmitFisrtBarline: int(3)
    Other: int


class Type(Enum):
    Circle: 0
    Slider: 1
    NewCombo: 2
    Spinner: 3
    OsuManiaHold: 7
    ComboColoursToSkip: int


class Color(Enum):
    Red: int
    Green: int
    Blue: int


class HitSound(Enum):
    Normal: 0
    Whistle: 1
    Finish: 2
    Clap: 3


class SampleSet(Enum):
    NoCustomSampleset: int(0)
    Normal: int(1)
    Soft: int(2)
    Drum: int(3)


class HitSample:
    normalSet: int #SampleSet
    additionSet: int  #SampleSet
    index: int
    volume: int
    filename: str


class ObjectParams:
    pass


class EventParams:
    pass


class General:
    AudioFilename: str = None
    AudioLeadIn: int = 0
    AudioHash: str = None
    PreviewTime: int = -1
    Countdown: int = 1
    SampleSet: str = "Normal"  #SampleSet.Normal.value
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


class Editor:
    Bookmarks: List[int]
    DistanceSpacing: float = None
    BeatDivisor: int = None
    GridSize: int = None
    TimelineZoom: float = None


class Metadata:
    Title: str = None
    TitleUnicode: str = None
    Artist: str = None
    ArtistUnicode: str = None
    Creator: str = None
    Version: str = None
    Source: str = None
    Tags: List[str]
    BeatmapID: int = None
    BeatmapSetID: int = None


class Difficulty:
    HPDrainRate: float = None
    CircleSize: float = None
    OverallDifficulty: float = None
    ApproachRate: float = None
    SliderMultiplier: float = None
    SliderTickRate: float = None



class Event:
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


class TimingPoint:
    time: int = None
    beatLength: float = None
    meter: int = None
    sampleSet: int = 1   # SampleSet = SampleSet.Normal.value
    sampleIndex: int = 0
    volume: int = None
    uninherited: int = None
    effects: int = 0  # Effect = None
    bpm: int = None

    def calculate_bpm(self):
        self.bpm = round(60000 / self.beatLength)


# TODO check wiki for colours
class ColourObject:
    Combo: int
    color: Color

    # SliderTrackOverride
    # SliderBorder

class Cercle(ObjectParams):
    pass


class SliderCurve(Enum):
    Besier: "B"
    Catmull: "C"
    Linear: "L"
    PerfectCircle: "P"


class Slider(ObjectParams):
    curveType: str
    curvePoints: str  # TODO
    slides: int
    length: float
    edgeSounds: str  # TODO
    edgeSets: str  # TODO


class Spinner(ObjectParams):
    endTime: int
    hitSample: HitSample


class HitObject:
    x: int
    y: int
    time: int
    type: int = 0 # Type
    hitSound: HitSound
    objectParams: Optional[ObjectParams]
    hitSample: Optional[HitSample]


class Structure:
    file_format: str
    general: General
    editor: Editor
    metadata: Metadata
    difficulty: Difficulty
    events: Event
    timing_points: List[TimingPoint]
    colours: List[ColourObject]
    hit_objects: List[HitObject]

    # def __int__(self, ile_format: str,
    #             general: General,
    #             editor: Editor,
    #             metadata: Metadata,
    #             difficulty: Difficulty,
    #             events: Event,
    #             timing_points: List[TimingPoint],
    #             colours: List[ColourObject],
    #             hit_objects: List[HitObject]):
    #
    #     self.ile_format = ile_format
    #     self.general = general
    #     self.editor = editor
    #     self.metadata = metadata
    #     self.difficulty = difficulty
    #     self.events = events
    #     self.timing_points = timing_points
    #     self.colours = colours
    #     self.hit_objects = hit_objects



    # def __init__(self, **entries):
    #     self.__dict__.update(entries)
    # General(**self.general)
