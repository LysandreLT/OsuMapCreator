# create a beatmap set to give to the UI segment
from typing import List, Optional

from MapCreator.Utils.models.models import General, Editor, Metadata, Difficulty, HitObject, SectionName


class BeatmapSet:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_format = ""
        self.general = None
        self.editor = None
        self.metadata = None
        # self.difficulty = Difficulty()
        # self.events: List[Event] = []
        # self.timing_points: List[TimingPoint] = []
        # self.colours: List[ColourObject] = []
        self.hit_objects: List[HitObject] = []

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

        resultList = [key + ":" + str(value)+"\n" for key, value in self.general.__dict__.items() if value != None]
        self.write_append(self.file_name,SectionName.General.value+"\n")
        self.write_append(self.file_name, resultList)

    def build_editor(self,
                     Bookmarks: Optional[List[int]] = None,
                     DistanceSpacing: Optional[float] = None,
                     BeatDivisor: Optional[int] = None,
                     GridSize: Optional[int] = None,
                     TimelineZoom: Optional[float] = None):
        self.editor = Editor(Bookmarks=Bookmarks,
                             DistanceSpacing=DistanceSpacing,
                             BeatDivisor=BeatDivisor,
                             GridSize=GridSize,
                             TimelineZoom=TimelineZoom)

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
        self.write_append(self.file_name, "\n"+SectionName.Metadata.value + "\n")
        self.write_append(self.file_name, resultList)

    def build_hit_points(self, hit_points: List[HitObject]):
        resultList = []
        for hit_obj in hit_points:
            r = hit_obj.__str__() + "\n"
            resultList.append(r)
        self.write_append(self.file_name,"\n"+SectionName.HitObjects.value + "\n")
        self.write_append(self.file_name, resultList)

    def build_beatmap_test(self):
        self.file_format = "osu file format v14\n\n"
        self.write_append(self.file_name,self.file_format)
        self.build_general(AudioFilename="audio.mp3")
        self.build_editor()
        self.build_metadata(Title="test")

    def build_beatmap_set(self):
        # cretae folder in the dest path
        # put the audio
        # put the beatmap
        # zip all

        pass




    def write_append(self, file_name, lines):
        with open(file_name, 'a') as f:
            f.writelines(lines)


if __name__ == "__main__":
    file_name = "test.osu"
    beatmapset = BeatmapSet(file_name)
    beatmapset.build_beatmap_test()
