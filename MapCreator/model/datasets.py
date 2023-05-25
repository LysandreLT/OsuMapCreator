import numpy
import pandas as pd
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import glob
import cv2
import os

from MapCreator.Utils.models.models import Spinner, Cercle, Slider
from MapCreator.Utils.parser import Parse


def load_beatmap_attributes(path):
    cols = ["x", "y", "time", "type", "endtime", "x2", "2", "x3", "y3", "x4", "y4", "slide", "length"]

    parser = Parse()
    parser.parse_file(path)

    x = []
    y = []
    time = []
    type = []
    endtime = []
    x2 = []
    y2 = []
    x3 = []
    y3 = []
    x4 = []
    y4 = []
    x5 = []
    y5 = []
    slide = []
    length = []

    for o in parser.hit_objects:
        x.append(o.x)
        y.append(o.y)
        time.append(o.time)
        type.append(o.type)
        if isinstance(o, Cercle):
            endtime.append(0)
            x2.append(0)
            y2.append(0)
            x3.append(0)
            y3.append(0)
            x4.append(0)
            y4.append(0)
            slide.append(0)
            length.append(0)
        elif isinstance(o, Spinner):
            endtime.append(o.endTime)
            x2.append(0)
            x2.append(0)
            x3.append(0)
            x3.append(0)
            x4.append(0)
            x4.append(0)
            slide.append(0)
            length.append(0)
        elif isinstance(o, Slider):
            endtime.append(0)
            x2.append(o.curvePoints[0].x)
            y2.append(o.curvePoints[0].y)

            if len(o.curvePoints) > 1:
                x3.append(o.curvePoints[1].x)
                y3.append(o.curvePoints[1].y)
            else:
                x3.append(0)
                y3.append(0)

            if len(o.curvePoints) > 2:
                x4.append(o.curvePoints[2].x)
                y4.append(o.curvePoints[2].y)
            else:
                x4.append(0)
                y4.append(0)

            slide.append(o.slides)
            length.append(o.length)
        else:
            endtime.append(0)
            x2.append(0)
            y2.append(0)
            x3.append(0)
            y3.append(0)
            x4.append(0)
            y4.append(0)
            slide.append(0)
            length.append(0)

    d = [x, y, time, type, endtime, x2, y2, x3, y3, x4, y4, slide, length]

    df_t = pd.DataFrame(d).T
    df = pd.DataFrame(df_t.values.tolist(), columns=cols)
    df.drop(df.tail(1).index,
            inplace=True)
    print(df.to_numpy())
    return df


def load_beatmaps(paths):
    arr = []
    for path in paths:
        df_temp = load_beatmap_attributes(path)
        arr.append(df_temp)
    df = pd.DataFrame(arr)
    return df


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


def load_spectrogramm_image(paths):
    # image = np.zeros((64, 64, 3), dtype="uint8")
    images = []
    for path in paths:
        image = cv2.imread(path)
        images.append(image)
    return np.array(images)


if __name__ == "__main__":
    PATH1 = "C:/Users/hugob/dev/python/OsuMapCreator/MapCreator/datasets/maps/552854 REOL - YoiYoi Kokon/REOL - YoiYoi Kokon (Ongaku) [Hyperion's Overdose].osu"
    PATH2 = "C:/Users/hugob/dev/python/OsuMapCreator/MapCreator/datasets/maps/552854 REOL - YoiYoi Kokon/REOL - YoiYoi Kokon (Ongaku) [Hyperion's Overdose].osu"
    PATH3 = "C:/Users/hugob/dev/python/OsuMapCreator/MapCreator/datasets/maps/552854 REOL - YoiYoi Kokon/REOL - YoiYoi Kokon (Ongaku) [Hyperion's Rain].osu"
    PATH = [PATH3, PATH2, PATH1]
