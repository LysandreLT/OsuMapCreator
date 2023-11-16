from keras import layers
from tensorflow import keras
from MapCreator.Utils.trainingMapParser import *

base_path = "/MapCreator/datasets"
paths = get_paths(os.path.join(base_path, "maps"))
df, spectrograms, diff = load_beatmaps_and_spectrograms(paths)
x_train = spectrograms
x_train = np.array(x_train, dtype=float)
y_train = df
y_train = np.array(y_train, dtype=float)
decoder_input = np.zeros((len(y_train), 4001, 13))

# Ajout des tokens de début et de fin de séquence
index = 0
start_of_sequence = np.array([-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0])
end_of_sequence = np.array([-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2]).reshape((1, 1, -1))
end_of_sequence = np.repeat(end_of_sequence, len(y_train), axis=0)

for sublist in decoder_input:
    sublist[0] = start_of_sequence
    sublist[1:] = y_train[index]

y_train = np.append(y_train, end_of_sequence, axis=1)
print(y_train[0][-1])

print("Taille de l'input d'entraînement : " + str(x_train.shape))
print("Taille de l'output d'entraînement : " + str(y_train.shape))

input_dim = 128
decoder_input_shape = 13
latent_dim = 256

# Model's input
input_spectrogram = keras.Input((20000, 128, 1), name="input_spectrogram")
# Convolution layer 1
x = layers.Conv2D(
    filters=64,
    kernel_size=[11, 41],
    strides=[2, 2],
    padding="same",
    use_bias=False,
    name="conv_1",
)(input_spectrogram)
x = layers.BatchNormalization(name="conv_1_bn")(x)
x = layers.ReLU(name="conv_1_relu")(x)
# Convolution layer 2
x = layers.Conv2D(
    filters=64,
    kernel_size=[11, 21],
    strides=[1, 2],
    padding="same",
    use_bias=False,
    name="conv_2",
)(x)
x = layers.BatchNormalization(name="conv_2_bn")(x)
x = layers.ReLU(name="conv_2_relu")(x)

encoder = keras.layers.LSTM(latent_dim, return_state=True)
encoder_outputs, state_h, state_c = encoder(x)

# We discard `encoder_outputs` and only keep the states.
encoder_states = [state_h, state_c]

# Set up the decoder, using `encoder_states` as initial state.
decoder_inputs = keras.Input(shape=(None, decoder_input_shape), name="input_teacher_forcing")

# We set up our decoder to return full output sequences,
# and to return internal states as well. We don't use the
# return states in the training model, but we will use them in inference.
decoder_lstm = keras.layers.LSTM(latent_dim, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)
decoder_dense = layers.Dense(13, activation='relu')
decoder_outputs = decoder_dense(decoder_outputs)

# Define the model that will turn
# `encoder_input_data` & `decoder_input_data` into `decoder_target_data`
model = keras.Model([input_spectrogram, decoder_inputs], decoder_outputs)

model.compile(
    optimizer="adam",
    loss=keras.losses.MeanAbsoluteError(),
)
# model.summary()


# model.fit(
#     [x_train, decoder_input],
#     y_train,
#     batch_size=1,
#     epochs=50,
#     # validation_split=0.2
# )

# Save model
model.save("MapCreator")
print("Sauvegarde du modèle terminée")
