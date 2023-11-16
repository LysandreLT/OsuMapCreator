from tensorflow import keras

"""
Entrées : 
Sortie : .txt
"""

latent_dim = 256
input_dim = 128

model = keras.models.load_model("../MapCreator")

# Encoder
encoder_inputs = model.input[0]  # input_1
encoder_outputs, state_h_enc, state_c_enc = model.layers[10].output  # lstm_1
encoder_states = [state_h_enc, state_c_enc]
encoder_model = keras.Model(encoder_inputs, encoder_states)

# Decoder
decoder_inputs = model.input[1]  # input_2
decoder_state_input_h = keras.Input(shape=(latent_dim,))
decoder_state_input_c = keras.Input(shape=(latent_dim,))
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]

decoder_lstm = model.layers[11]
decoder_outputs, state_h_dec, state_c_dec = decoder_lstm(
    decoder_inputs, initial_state=decoder_states_inputs
)
decoder_states = [state_h_dec, state_c_dec]
decoder_dense = model.layers[12]
decoder_outputs = decoder_dense(decoder_outputs)
decoder_model = keras.Model(
    [decoder_inputs] + decoder_states_inputs, [decoder_outputs] + decoder_states
)


def sampling(input_seq):
    # Encode the input as state vectors.
    states_value = encoder_model.predict(input_seq)
    target_seq = np.array([-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]).reshape(
        (1, 1, -1))
    print(states_value[0].shape)
    # Sampling loop for a batch of sequences
    # (to simplify, here we assume a batch of size 1).
    stop_condition = False
    decoded_sample = []
    while not stop_condition:
        output_element, h, c = decoder_model.predict([target_seq] + states_value)

        decoded_sample.append(output_element)

        # Exit condition: either hit max length
        # or find stop character.
        if output_element == [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] \
                or len(decoded_sample) > 4000:
            stop_condition = True

        # Update the target sequence (of length 1).
        target_seq = output_element

        # Update states
        states_value = [h, c]
    return decoded_sample


if __name__ == "__main__":
    from MapCreator.Utils.trainingMapParser import *
    base_path = "/MapCreator/datasets"
    paths = get_paths(os.path.join(base_path, "maps"))
    df, spectrograms, diff = load_beatmaps_and_spectrograms(paths)
    x_train = spectrograms
    x_train = np.array(x_train, dtype=float)
    print(x_train[0].shape)
    sampling(x_train[0])
