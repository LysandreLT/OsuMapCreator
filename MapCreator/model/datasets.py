import os.path

import cv2
import librosa
import numpy as np
import pandas as pd
import skimage
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import MinMaxScaler

from MapCreator.Utils.models.models import Spinner, Cercle, Slider
from MapCreator.Utils.parser import Parse


def load_beatmap_attributes(path):
    cols = ["x", "y", "time", "type", "endtime", "x2", "2", "x3", "y3", "x4", "y4", "slide", "length"]

    parser = Parse()
    parser.parse_file(path)
    max_hit_object = 2000
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
        print(path[0])
        df_temp, difficulty = load_beatmap_attributes(path[0])
        print(df_temp.shape)
        arr.append(df_temp)
        diff.append(difficulty)
    print(np.array(arr, dtype=object).shape)
    diff = np.array(diff, dtype=float)
    df = np.asarray(arr, dtype=object)
    return df, diff


def process_beatmaps_attributes(df, train, test):
    # initialize the column names of the continuous data
    continuous = ["bedrooms", "bathrooms", "area"]
    # performin min-max scaling each continuous feature column to
    # the range [0, 1]
    cs = MinMaxScaler()
    trainContinuous = cs.fit_transform(train[continuous])
    testContinuous = cs.transform(test[continuous])
    # one-hot encode the zip code categorical data (by definition of
    # one-hot encoding, all output features are now in the range [0, 1])
    zipBinarizer = LabelBinarizer().fit(df["zipcode"])
    trainCategorical = zipBinarizer.transform(train["zipcode"])
    testCategorical = zipBinarizer.transform(test["zipcode"])
    # construct our training and testing data points by concatenating
    # the categorical features with the continuous features
    trainX = np.hstack([trainCategorical, trainContinuous])
    testX = np.hstack([testCategorical, testContinuous])
    # return the concatenated training and testing data
    return (trainX, testX)


def scale_minmax(X, min=0.0, max=1.0):
    X_std = (X - X.min()) / (X.max() - X.min())
    X_scaled = X_std * (max - min) + min
    return X_scaled


def create_images(paths, base_path):
    for p in paths:
        temp = f"{base_path}/images/{os.path.basename(os.path.dirname(p[1]))}.png"
        if os.path.exists(temp):
            pass
        else:
            create_image(p[1])


def create_image(audio_path):
    # settings
    hop_length = 512  # number of samples per time-step in spectrogram
    n_mels = 128  # number of bins in spectrogram. Height of image
    time_steps = 384  # number of time-steps. Width of image

    # load audio. Using example from librosa

    y, sr = librosa.load(audio_path, sr=44100)
    out_pure_data = f"C:/Users/hugob/dev/python/OsuMapCreator/MapCreator/datasets/images/{os.path.basename(os.path.dirname(audio_path))}.png"

    # extract a fixed length window
    start_sample = 0  # starting at beginning
    length_samples = time_steps * hop_length
    # window = y[start_sample:start_sample + length_samples]
    window = y
    # convert to PNG
    spectrogram_image(window, sr=sr, out=out_pure_data, hop_length=hop_length, n_mels=n_mels)
    print('wrote file', out_pure_data)


def spectrogram_image(y, sr, out, hop_length, n_mels):
    # use log-melspectrogram
    mels = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels,
                                          n_fft=hop_length * 2, hop_length=hop_length)
    mels = np.log(mels + 1e-9)  # add small number to avoid log(0)

    # min-max scale to fit inside 8-bit range
    img = scale_minmax(mels, 0, 255).astype(np.uint8)
    img = np.flip(img, axis=0)  # put low frequencies at the bottom in image
    img = 255 - img  # invert. make black==more energy

    # save as PNG
    skimage.io.imsave(out, img)


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


def load_spectrogramm_image(paths):
    # image = np.zeros((64, 64, 3), dtype="uint8")
    images = []
    for path in paths:
        image = cv2.imread(path)
        images.append(image)
    return np.array(images)


if __name__ == "__main__":
    base_path = "C:/Users/hugob/dev/python/OsuMapCreator/MapCreator/datasets"
    paths = get_paths(base_path + "/maps")
    df, diff = load_beatmaps(paths)
    create_images(paths, base_path)
