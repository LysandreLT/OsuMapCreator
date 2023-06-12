import os.path
from typing import List

import numpy as np

from MapCreator.Utils.models.models import Spinner, Cercle, Slider, HitObject
from MapCreator.Utils.parser import Parser
from MapCreator.Utils.audio import load_melspectrogram


def scale_beatmap(hitpoints: List[HitObject]):
    # we take 7min30s for each beatmap
    duration = 7.739984882842026 * 60
    new_hitpoints = []
    for h in hitpoints:
        if h.time <= duration * 1000:
            new_hitpoints.append(h)
    # hitpoints = [x for x in hitpoints if x[2] <= duration * 1000]
    return new_hitpoints


def load_beatmap_attributes(path, max_hit_object=4000):
    cols = ["x", "y", "time", "type", "endtime", "x2", "y2", "x3", "y3", "x4", "y4", "slide", "length"]
    parser = Parser()
    parser.parse_file(path)

    hitpoints = scale_beatmap(parser.hit_objects)

    if max_hit_object is None:
        max_hit_object = len(hitpoints)
    data = np.zeros((13, max_hit_object), dtype=int)

    for (i, o) in enumerate(hitpoints):

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


def load_beatmaps_and_spectrograms(paths: List, max=1000):
    arr = []
    diff = []
    spectrograms = []
    for i, path in enumerate(paths):
        if max and i >= max:
            break
        spectrogram = path_to_audio(path[1])
        for beatmap in path[0]:
            df_temp, difficulty = load_beatmap_attributes(beatmap)
            df_temp = df_temp.transpose()
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


def get_paths(dir_path, max=1000):
    file_paths = []

    for i, dir in enumerate(os.listdir(dir_path)):
        if max and i >= max:
            break
        audio = ""
        beatmaps = []
        for file in os.listdir(os.path.join(dir_path, dir)):
            if file.endswith(".mp3") or file.endswith(".wav"):
                audio = os.path.join(dir_path, dir, file)
            elif file.endswith(".osu"):
                beatmaps.append(os.path.join(dir_path, dir, file))
        file_paths.append((beatmaps, audio))

    return file_paths


if __name__ == "__main__":
    base_path = "C:/Users/Lysandre/Documents/GitHub/OsuMapCreator/MapCreator/datasets"
    paths = get_paths(os.path.join(base_path, "maps"))
    data = load_beatmap_attributes(paths[0][0][0])
    print(data)
