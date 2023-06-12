# create a beatmap set to give to the UI segment
import math
import os.path
import random
from typing import List, Optional

import librosa

from MapCreator.Utils.models.models import General, Editor, Metadata, Difficulty, HitObject, SectionName, Circle, Event, \
    TimingPoint, Slider, Spinner, CurvePoint
from MapCreator.music import audio_
from MapCreator.music.audio_ import compute_bpm, load


class BeatmapSet:
    def __init__(self):
        self.file_name = ""
        self.file_format = ""
        self.general: General = None
        self.editor: Editor = None
        self.metadata: Metadata = None
        self.difficulty: Difficulty = None
        self.events: Event = None
        self.timing_points: List[TimingPoint] = []
        self.colours = None
        self.hit_objects: List[HitObject] = None

    def build_general(self,
                      AudioFilename: str,
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
        self.general = General(AudioFilename=AudioFilename,
                               AudioHash=AudioHash,
                               AudioLeadIn=AudioLeadIn,
                               PreviewTime=PreviewTime,
                               Countdown=Countdown,
                               SampleSet=SampleSet,
                               StackLeniency=StackLeniency,
                               Mode=Mode,
                               LetterboxInBreaks=LetterboxInBreaks,
                               StoryFireInFront=StoryFireInFront,
                               UseSkinSprites=UseSkinSprites,
                               AlwaysShowPlayfield=AlwaysShowPlayfield,
                               OverlayPosition=OverlayPosition,
                               SkinPreference=SkinPreference,
                               EpilepsyWarning=EpilepsyWarning,
                               CountdownOffset=CountdownOffset,
                               SpecialStyle=SpecialStyle,
                               WidescreenStoryboard=WidescreenStoryboard,
                               SamplesMatchPlaybackRate=SamplesMatchPlaybackRate)

        resultList = [key + ":" + str(value) + "\n" for key, value in self.general.__dict__.items() if value != None]
        self.write_append(self.file_name, SectionName.General.value + "\n", 'a')
        self.write_append(self.file_name, resultList, 'a')

    def build_editor(self,
                     Bookmarks: Optional[List[int]] = None,
                     DistanceSpacing: float = 1.22,
                     BeatDivisor: int = 4,
                     GridSize: int = 4,
                     TimelineZoom: float = 1.0):
        self.editor = Editor(Bookmarks=Bookmarks,
                             DistanceSpacing=DistanceSpacing,
                             BeatDivisor=BeatDivisor,
                             GridSize=GridSize,
                             TimelineZoom=TimelineZoom)
        resultList = [key + ":" + str(value) + "\n" for key, value in self.editor.__dict__.items() if value != None]
        self.write_append(self.file_name, "\n" + SectionName.Editor.value + "\n", 'a')
        self.write_append(self.file_name, resultList, 'a')

    def build_metadata(self,
                       Title: str,
                       TitleUnicode: Optional[str] = None,
                       Artist: Optional[str] = None,
                       ArtistUnicode: Optional[str] = None,
                       Creator: Optional[str] = None,
                       Version: Optional[str] = "Normal",
                       Source: Optional[str] = None,
                       Tags: Optional[List[str]] = None,
                       BeatmapID: Optional[int] = None,
                       BeatmapSetID: Optional[int] = None):
        self.metadata = Metadata(Title=Title,
                                 TitleUnicode=TitleUnicode,
                                 Artist=Artist,
                                 ArtistUnicode=ArtistUnicode,
                                 Creator=Creator,
                                 Version=Version,
                                 Source=Source,
                                 Tags=Tags,
                                 BeatmapID=BeatmapID,
                                 BeatmapSetID=BeatmapSetID)
        resultList = [key + ":" + str(value) + "\n" for key, value in self.metadata.__dict__.items() if value != None]
        self.write_append(self.file_name, "\n" + SectionName.Metadata.value + "\n", 'a')
        self.write_append(self.file_name, resultList, 'a')

    def build_difficulty(self,
                         HPDrainRate: float = 5.0,
                         CircleSize: float = 5.0,
                         OverallDifficulty: float = 5.0,
                         ApproachRate: float = 5.0,
                         SliderMultiplier: float = 1.4,
                         SliderTickRate: float = 1.0):
        self.difficulty = Difficulty(HPDrainRate=HPDrainRate,
                                     CircleSize=CircleSize,
                                     OverallDifficulty=OverallDifficulty,
                                     ApproachRate=ApproachRate,
                                     SliderMultiplier=SliderMultiplier,
                                     SliderTickRate=SliderTickRate)
        resultList = [key + ":" + str(value) + "\n" for key, value in self.difficulty.__dict__.items() if value != None]
        self.write_append(self.file_name, "\n" + SectionName.Difficulty.value + "\n", 'a')
        self.write_append(self.file_name, resultList, 'a')

    def build_events(self):
        events = ["[Events]",
                    "//Background and Video events",
                    "//Storyboard Layer 0 (Background)",
                    "//Storyboard Layer 1 (Fail)",
                    "//Storyboard Layer 2 (Pass)",
                    "//Storyboard Layer 3 (Foreground)",
                    "//Storyboard Layer 4 (Overlay)",
                    "//Storyboard Sound Samples"]
        resultList = [x + "\n" for x in events]
        self.write_append(self.file_name, resultList, 'a')

    # [TimingPoints]
    # time , beatlength, meter, sampleset (nornal = 1), sampleIndex (default = 0), volume (= 100%), uninherited,effects
    # 8692.70490823524, 428.571428571429, 4, 1, 0, 100, 1, 0 --> 60 * 1000 / 428.571 = 140 BPM --> 60 000 / BPM = beatLength
    def build_timing_point(self, y, sr, **kwargs):
        resultList = []
        tempo = audio_.bpm(y, sr)
        beatlength = 60000 / tempo
        t = TimingPoint(time=0, beatLength=int(beatlength), meter=4, sampleSet=1, sampleIndex=0, volume=100,
                        uninherited=1,
                        effects=0)
        self.timing_points.append(t)
        resultList = [x.__str__() + "\n" for x in self.timing_points]
        self.write_append(self.file_name, "\n" + SectionName.TimingPoints.value + "\n", 'a')
        self.write_append(self.file_name, resultList, 'a')

    def build_hitobjects_and_timingpoints(self, audio, difficulty):
        y, sr = load(audio)
        self.build_timing_point(y, sr)
        self.build_hit_points(y, sr, difficulty)

    # 512 * 384
    def build_hit_points(self, y, sr, difficulty):
        def random_position(x1, y1, distance) -> CurvePoint:
            padding = 50
            angle = random.randrange(0, 360, 5)
            angle_rad = math.radians(angle)

            x = x1 + distance * math.cos(angle_rad)
            y = y1 + distance * math.sin(angle_rad)

            # if (x > 512 - padding) or (y > 384 - padding) or (x < 0 + padding) or (y < 0 + padding):
            #     if recursion > 10:
            #         return CurvePoint(x=256, y=192)
            #     random_position(x1, y1, distance, recursion + 1)
            if y < padding:
                y = y + abs(y) + padding
            if x < padding:
                x = x + abs(x) + padding
            while y > 384 - padding:
                y -= padding
            while x > 512 - padding:
                x -= padding

            return CurvePoint(x=int(x), y=int(y))

        def is_time_between_2_points_enough(time1, time2, _difficulty):
            if time1 - time2 > _difficulty * 1000:
                return True
            return False

        onsets = audio_.compute_onset_superflux(y, sr)

        resultList: List[HitObject] = []
        n = 0

        while n < len(onsets):
            index = len(resultList)

            rvalue = random.randrange(1, 3, 1)

            if n == len(onsets) - 1:
                hit_point = Spinner(x=256, y=192, time=round(onsets[n]), type=12, hitSound=0,
                                    endTime=round(onsets[n]) + 3000)
                resultList.append(hit_point)

                n += 1
            elif n == 0:

                hit_point = Circle(x=256, y=192, time=round(onsets[n]), type=5, hitSound=0)
                resultList.append(hit_point)

                n += 1
            elif n != 0 and is_time_between_2_points_enough(onsets[n], round(onsets[n - 1]), difficulty):

                if rvalue == 1:
                    curve_type = random.choice(["B", "C", "L", "P"])
                    p = random_position(resultList[index - 1].x, resultList[index - 1].y, random.randrange(40, 60, 1))

                    curve_points: List[CurvePoint] = []
                    curve_point_nb: int = 0
                    edge_sets = "0:0|0:0"
                    edge_sounds = "2|2"
                    # TODO
                    # length = self.timing_point(onsets[n])
                    length = self.timing_points[0].beatLength

                    if curve_type == "P":
                        curve_point_nb = 2
                    elif curve_type == "L":
                        curve_point_nb = 1
                    else:
                        curve_point_nb = random.randrange(2, 4, 1)

                    for i in range(0, curve_point_nb):
                        if i == 0:
                            cp = random_position(p.x, p.y, random.randrange(40, 60, 1))
                            curve_points.append(cp)
                        else:
                            cp = random_position(curve_points[i - 1].x, curve_points[i - 1].y,
                                                 random.randrange(40, 60, 1))
                            curve_points.append(cp)

                    hit_point = Slider(x=p.x, y=p.y, time=round(onsets[n]),
                                       type=2, hitSound=0, curveType=curve_type, curvePoints=curve_points, slides=1,
                                       length=length, edgeSounds=edge_sounds, edgeSets=edge_sets)

                    resultList.append(hit_point)
                    n += curve_point_nb + 1
                else:

                    p = random_position(resultList[index - 1].x, resultList[index - 1].y, random.randrange(40, 80, 1))
                    hit_point = Circle(x=p.x, y=p.y, time=round(onsets[n]), type=5, hitSound=0)
                    resultList.append(hit_point)

                    n += 1
            elif not is_time_between_2_points_enough(onsets[n], round(onsets[n - 1]), difficulty):
                n += 1

        self.write_append(self.file_name, "\n" + SectionName.HitObjects.value + "\n", 'a')

        resultList = [x.__str__() + "\n" for x in resultList]
        self.write_append(self.file_name, resultList, 'a')

    def write_append(self, file_name, lines, mode):
        with open(file_name, mode) as f:
            f.writelines(lines)


if __name__ == "__main__":
    audio = "C:/Users/hugob/dev/python/OsuMapCreator/MapCreator/datasets/maps/552854 REOL - YoiYoi Kokon/audio.mp3"
    y, sr = load(audio)
    # audio = audio_.compute_local_bpm(y, sr)
    # current_bpm = 0
    # beats = []
    # for i in range(len(audio[0])):
    #     if current_bpm != audio[0][i]:
    #         current_bpm = audio[0][i]
    #         beats.append((current_bpm, audio[1][i]))
    #
    # for beat in beats[1:]:
    #     print("tempo : ", beat[0], " | time :", beat[1])
    #
    # bpm = audio_.bpm(y,sr)
    # print("bpm : ", bpm)
