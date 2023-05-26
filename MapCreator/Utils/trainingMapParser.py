import os.path
import numpy as np
import pandas as pd

from MapCreator.Utils.models import Spinner, Cercle, Slider
from MapCreator.Utils.parser import Parser


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

    df_t = pd.DataFrame(data).T
    df = pd.DataFrame(df_t.values.tolist(), columns=cols)
    df = pd.DataFrame(df.values.tolist()).T
    # df.drop(df.tail(1).index,
    #         inplace=True)
    # print(df.loc[len(parser.hit_objects), :])
    return df.to_numpy(dtype=object), parser.difficulty.OverallDifficulty


def load_beatmaps(paths):
    arr = []
    diff = []
    for path in paths:
        df_temp, difficulty = load_beatmap_attributes(path[0])
        print(df_temp.shape)
        arr.append(df_temp)
        diff.append(difficulty)
    print(np.array(arr, dtype=object).shape)
    diff = np.array(diff, dtype=float)
    df = np.asarray(arr, dtype=object)
    return df, diff


def scale_minmax(X, min=0.0, max=1.0):
    X_std = (X - X.min()) / (X.max() - X.min())
    X_scaled = X_std * (max - min) + min
    return X_scaled


def get_paths(dir_path):
    file_paths = []
    audio_path = ""
    for root, directories, files in os.walk(dir_path):
        for filename in files:
            # join the two strings in order to form the full filepath.
            if filename.endswith(".mp3"):
                audio_path = os.path.join(root, filename)
            else:
                if audio_path != "":
                    filepath = os.path.join(root, filename)
                    file_paths.append((filepath, audio_path))

    # returning all file paths
    return file_paths



if __name__ == "__main__":
    base_path = "C:/Users/Lysandre/Documents/GitHub/OsuMapCreator/MapCreator/datasets/maps"
    paths = get_paths(base_path + "/maps")
    print(paths)
    df, diff = load_beatmaps(paths)
    print(df)
    print(diff)
