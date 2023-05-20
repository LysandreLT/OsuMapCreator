from ElementPlacementIA import ElementPlacement
from MapCreator.Utils.audio import *


sr, music = read("C:/Users/Lysandre/Documents/GitHub/OsuMapCreator/MapCreator/datasets/Musics/Smile-mileS (feat. なすお☆).mp3")


IA = ElementPlacement(20000, 25000000)
beatmap = IA.generate_beatmap(music)
