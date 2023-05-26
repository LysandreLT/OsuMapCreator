import tensorflow as tf


"""
Unet, deeplearning
Entrées : .txt, .MP3 (x minutes max)
Sortie : .txt
"""


def getModel():
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(2000000, activation='relu'))
    model.add(tf.keras.layers.Dense(200000, activation='relu'))
    model.add(tf.keras.layers.Dense(20000, activation='relu'))
    model.add(tf.keras.layers.Dense(10000, activation='relu'))
    model.add(tf.keras.layers.Dense(5000))
    return model

