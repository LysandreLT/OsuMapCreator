from enum import Enum
from typing import List

import decimal


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
    kiai_time: int(0)
    omit_fisrt_barline: int(3)
    other: int


class Type(Enum):
    Circle: 0
    Slider: 1
    new_combo: 2
    Spinner: 3
    osu_mania_hold: 7
    combo_colours_to_skip: int


class Color(Enum):
    red: int
    green: int
    blue: int


class HitSound(Enum):
    Normal: 0
    Whistle: 1
    Finish: 2
    Clap: 3


class SampleSet(Enum):
    no_custom_sampleset: int(0)
    normal: int(1)
    soft: int(2)
    Drum: int(3)


class HitSample:
    normalSet: SampleSet
    additionSet: SampleSet
    index: int
    volume: int
    filename: str


class ObjectParams:
    pass


class EventParams:
    pass


class General:
    AudioFilename: str
    AudioLeadIn: int
    AudioHash: str
    PreviewTime: int
    Countdown: int
    SampleSet: str
    StackLeniency: decimal
    Mode: int
    LetterboxInBreaks: int
    StoryFireInFront: int
    UseSkinSprites: int
    AlwaysShowPlayfield: int
    OverlayPosition: str
    SkinPreference: str
    EpilepsyWarning: int
    CountdownOffset: int
    SpecialStyle: int
    WidescreenStoryboard: int
    SamplesMatchPlaybackRate: int

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def expand(self):
        return self


class Editor:
    Bookmarks: List[int]
    DistanceSpacing: decimal
    BeatDivisor: int
    GridSize: int
    TimelineZoom: decimal

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def expand(self):
        return self


class Metadata:
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

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def expand(self):
        return self


class Difficulty:
    HPDrainRate: decimal
    CircleSize: decimal
    OverallDifficulty: decimal
    ApproachRate: decimal
    SliderMultiplier: decimal
    SliderTickRate: decimal

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def expand(self):
        return self


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
    time: int
    beatLength: decimal
    meter: int
    sampleSet: int
    sampleIndex: int
    volume: int
    uninherited: int
    effects: Effect
    bpm: int

    def expand(self):
        return self

    def calculate_bpm(self):
        self.bpm = round(60000 / self.beatLength)


# TODO check wiki for colours
class ColourObject:
    Combo: int
    color: Color

    # SliderTrackOverride
    # SliderBorder
    def expand(self):
        return self


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
    length: decimal
    edgeSounds: str  # TODO
    edgeSets: str  # TODO


class Spinner(ObjectParams):
    endTime: int
    hitSample: HitSample


class HitObject:
    x: int
    y: int
    time: int
    type: Type
    hitSound: HitSound
    objectParams: ObjectParams
    hitSample: HitSample

    def expand(self):
        return self


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

    def __int__(self, ile_format: str,
                general: General,
                editor: Editor,
                metadata: Metadata,
                difficulty: Difficulty,
                events: Event,
                timing_points: List[TimingPoint],
                colours: List[ColourObject],
                hit_objects: List[HitObject]):

        self.ile_format = ile_format
        self.general = general
        self.editor = editor
        self.metadata = metadata
        self.difficulty = difficulty
        self.events = events
        self.timing_points = timing_points
        self.colours = colours
        self.hit_objects = hit_objects



    # def __init__(self, **entries):
    #     self.__dict__.update(entries)
    # General(**self.general)
