import numpy as np

from MapCreator.IA.ElementPlacementIA import build_model
from tensorflow import keras
from MapCreator.Utils.trainingMapParser import *

base_path = "C:/Users/Lysandre/Documents/GitHub/OsuMapCreator/MapCreator/datasets"
paths = get_paths(os.path.join(base_path, "maps"))
df, spectrograms, diff = load_beatmaps_and_spectrograms(paths)
x_train = spectrograms[:int(len(spectrograms) * 0.8)]
x_train = np.array(x_train, dtype=float)
y_train = df[:int(len(df) * 0.8)]
y_train = np.array(y_train, dtype=float)
decoder_input = np.zeros((len(y_train), 4001, 13))

# Ajout des tokens de début et de fin de séquence
index = 0
start_of_sequence = np.array([-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0])
end_of_sequence = np.array([-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2]).reshape((1, 1, -1))
end_of_sequence = np.repeat(end_of_sequence, 7, axis=0)

for sublist in decoder_input:
    sublist[0] = start_of_sequence
    sublist[1:] = y_train[index]

y_train = np.append(y_train, end_of_sequence, axis=1)
print(y_train[0][-1])

x_val = spectrograms[int(len(spectrograms) * 0.8):]
x_val = np.array(x_val, dtype=float)
y_val = df[int(len(df) * 0.8):]
y_val = np.array(y_val, dtype=float)
print("Taille de l'input d'entraînement : " + str(x_train.shape))
print("Taille de l'output d'entraînement : " + str(y_train.shape))
print("Taille de l'input du dataset de validation : " + str(x_val.shape))
print("Taille de l'output du dataset de validation : " + str(y_val.shape))
model = build_model(input_dim=128, decoder_input_shape=13, latent_dim=256)

model.compile(
    optimizer="adam",
    loss=keras.losses.MeanAbsoluteError(),
)
model.summary()

model.fit(
    [x_train, decoder_input],
    y_train,
    batch_size=64,
    epochs=5,
)
# Save model
model.save("OsuMapCreator")
