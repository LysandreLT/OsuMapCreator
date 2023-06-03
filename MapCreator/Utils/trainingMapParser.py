import os.path
from typing import List

import numpy as np
from numpy import shape

from MapCreator.Utils.models.models import Spinner, Cercle, Slider
from MapCreator.Utils.parser import Parser
from MapCreator.Utils.audio import load_melspectrogram


def load_beatmap_attributes(path):
    cols = ["x", "y", "time", "type", "endtime", "x2", "2", "x3", "y3", "x4", "y4", "slide", "length"]

    parser = Parser()
    parser.parse_file(path)
    max_hit_object = 4000
    data = np.zeros((13, max_hit_object), dtype=object)

    for (i, o) in enumerate(parser.hit_objects):

        if i < max_hit_object:

            data[0][i] = o.x
            data[1][i] = o.y
            data[2][i] = o.time
            data[3][i] = o.type

            if isinstance(o, Cercle):
                pass
            elif isinstance(o, Spinner):
                data[4][i] = o.endTime
            elif isinstance(o, Slider):
                data[5][i] = o.curvePoints[0].x
                data[6][i] = o.curvePoints[0].y

                if len(o.curvePoints) > 1:
                    data[7][i] = o.curvePoints[1].x
                    data[8][i] = o.curvePoints[1].y

                if len(o.curvePoints) > 2:
                    data[9][i] = o.curvePoints[2].x
                    data[10][i] = o.curvePoints[2].y

                data[11][i] = o.slides
                data[12][i] = o.length

    return data, parser.difficulty.OverallDifficulty


def load_beatmaps_and_spectrograms(paths: List):
    arr = []
    diff = []
    spectrograms = []
    for path in paths:
        df_temp, difficulty = load_beatmap_attributes(path[0])
        df_temp = df_temp.transpose()
        spectrogram = load_melspectrogram(path[1])
        spectrogram = normalize(spectrogram)
        arr.append(df_temp)
        diff.append(difficulty)
        spectrograms.append(spectrogram)
    diff = np.array(diff, dtype=float)
    return arr, spectrograms, diff


def normalize(img):
    '''
    Normalizes an array
    (subtract mean and divide by standard deviation)
    '''
    eps = 0.001
    if np.std(img) != 0:
        img = (img - np.mean(img)) / np.std(img)
    else:
        img = (img - np.mean(img)) / eps
    return img


def contains_any_index(root, a_list):
    for i, c in enumerate(a_list):
        if c.startswith(root):
            return i + 1
    return 0


def get_paths(dir_path):
    file_paths = []
    audio_paths = []
    for root, directories, files in os.walk(dir_path):
        for filename in files:
            if filename.endswith(".mp3"):
                audio_paths.append(os.path.join(root, filename))
    for root, directories, files in os.walk(dir_path):
        for filename in files:
            if not filename.endswith(".mp3"):
                filepath = os.path.join(root, filename)
                audio_path_index = contains_any_index(root, audio_paths)
                if not audio_path_index == 0:
                    file_paths.append((filepath, audio_paths[audio_path_index - 1]))
    # returning all file paths
    return file_paths


if __name__ == "__main__":
    base_path = "C:/Users/Lysandre/Documents/GitHub/OsuMapCreator/MapCreator/datasets"
    paths = get_paths(os.path.join(base_path, "maps"))
    df, spectrograms, diff = load_beatmaps_and_spectrograms(paths)
    print(len(df[4]))
