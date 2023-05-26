# import the necessary packages
from MapCreator.model import datasets
from MapCreator.model import models
from sklearn.model_selection import train_test_split
from keras.layers import Dense
from keras.models import Model
from keras.optimizers import Adam
from keras.layers import concatenate
import numpy as np
# import argparse
import locale
import os

# construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-d", "--dataset", type=str, required=True,
# 	help="path to input dataset of house images")
# args = vars(ap.parse_args())

# construct the path to the input .txt file that contains information
# on each house in the dataset and then load the dataset
print("[INFO] loading beatmap attributes...")
base_path = "C:/Users/hugob/dev/python/OsuMapCreator/MapCreator/datasets"

paths = datasets.get_paths(os.path.sep.join(base_path, "/maps"))
df, difficulty = datasets.load_beatmaps(paths)
# load the spectrogram images and then scale the pixel intensities to the
# range [0, 1]
print("[INFO] loading spectrogram images...")
images = datasets.load_spectrogramm_image(os.path.join(base_path, "/images"))
images = images / 255.0

# partition the data into training and testing splits using 75% of
# the data for training and the remaining 25% for testing
print("[INFO] processing data...")
split = train_test_split(df, images, difficulty, test_size=0.25, random_state=42)
(trainAttrX, testAttrX, trainImagesX, testImagesX, trainDifficultyX, testDifficultyX) = split


model = models.get_model(trainAttrX.shape[1],trainDifficultyX.shape[0])



# compile the model using mean absolute percentage error as our loss,
# implying that we seek to minimize the absolute percentage difference
# between our price *predictions* and the *actual prices*
opt = Adam(lr=1e-3, decay=1e-3 / 200)
model.compile(loss="mean_absolute_percentage_error", optimizer=opt)
# train the model
print("[INFO] training model...")
model.fit(
	x=[trainAttrX, trainImagesX,trainDifficultyX], y=trainAttrX,
	validation_data=([testAttrX, testImagesX, testDifficultyX], testAttrX),
	epochs=200, batch_size=8)
# make predictions on the testing data
print("[INFO] predicting house prices...")
preds = model.predict([testImagesX,testDifficultyX])

