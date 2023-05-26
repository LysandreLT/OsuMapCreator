from MapCreator.Utils.audio import read
from MapCreator.IA.ElementPlacementIA import getModel
from tensorflow import keras
from MapCreator.Utils.parser import *
from MapCreator.Utils.trainingMapParser import *


basePath = ""
paths = get_paths(basePath)
df, diff = load_beatmaps(paths)
(x_train, y_train), (x_test, y_test) =

model = getModel()

model.compile(
    optimizer=keras.optimizers.Adam,
    loss=keras.losses.MeanAbsoluteError(),
)

history = model.fit(
    x_train,
    y_train,
    batch_size=64,
    epochs=2,
    # We pass some validation for
    # monitoring validation loss and metrics
    # at the end of each epoch
    validation_data=(x_val, y_val),
)

sr, music = read(
    "C:/Users/Lysandre/Documents/GitHub/OsuMapCreator/MapCreator/datasets/Musics/Smile-mileS (feat. なすお☆).mp3")
print(music.shape)
