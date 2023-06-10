import tensorflow as tf
import numpy as np
import tensorflow_io as tfio
from MapCreator.Utils.models.models import Spinner, Cercle, Slider, HitObject
from typing import List
from MapCreator.Utils.parser import Parser
from MapCreator.Utils.trainingMapParser import get_paths, load_beatmap_attributes
import os.path


class VectorizeChar:
    def __init__(self, max_len=4000):
        self.max_len = max_len

    def __call__(self, text):
        return []


def load_beatmaps_and_musics(paths, max=1000):
    data = []
    diff = []
    for i, path in enumerate(paths):
        if i and i >= max:
            break
        for beatmap in path[0]:
            df_temp, difficulty = load_beatmap_attributes(beatmap)
            df_temp = df_temp.transpose()
            diff.append(difficulty)
            data.append({"audio": path[1], "text": df_temp})
    return data


def create_text_ds(data):
    text_ds = [_["text"] for _ in data]
    text_ds = tf.data.Dataset.from_tensor_slices(text_ds)
    return text_ds


def path_to_audio(path):
    # spectrogram using stft
    audio = tf.io.read_file(path)
    audio, _ = tfio.audio.decode_mp3(audio, 1)
    audio = tf.squeeze(audio, axis=-1)
    stfts = tf.signal.stft(audio, frame_length=200, frame_step=80, fft_length=256)
    x = tf.math.pow(tf.abs(stfts), 0.5)
    # normalisation
    means = tf.math.reduce_mean(x, 1, keepdims=True)
    stddevs = tf.math.reduce_std(x, 1, keepdims=True)
    x = (x - means) / stddevs
    audio_len = tf.shape(x)[0]
    # padding to 10 seconds
    pad_len = 2754
    paddings = tf.constant([[0, pad_len], [0, 0]])
    x = tf.pad(x, paddings, "CONSTANT")[:pad_len, :]
    return x


def create_audio_ds(data):
    flist = [_["audio"] for _ in data]
    audio_ds = tf.data.Dataset.from_tensor_slices(flist)
    audio_ds = audio_ds.map(
        path_to_audio, num_parallel_calls=tf.data.AUTOTUNE
    )
    return audio_ds


def create_tf_dataset(data, bs=4):
    audio_ds = create_audio_ds(data)
    text_ds = create_text_ds(data)
    ds = tf.data.Dataset.zip((audio_ds, text_ds))
    ds = ds.map(lambda x, y: {"source": x, "target": y})
    ds = ds.batch(bs)
    ds = ds.prefetch(tf.data.AUTOTUNE)
    return ds
