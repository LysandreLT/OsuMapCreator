import librosa
import matplotlib.pyplot as plt
import numpy as np
from numpy import ndarray


def compute_onset_default(path) -> ndarray:
    y, sr = librosa.load(path)

    # params
    hop_length = int(librosa.time_to_samples(1. / 200, sr=sr))

    # default
    # odf_default = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)
    onset_default = librosa.onset.onset_detect(y=y, sr=sr, hop_length=hop_length,
                                               units='time')

    return onset_default * 1000


def compute_onset_superflux(path) -> ndarray:
    y, sr = librosa.load(path)

    # params
    n_fft = 1024
    hop_length = int(librosa.time_to_samples(1. / 200, sr=sr))
    lag = 2
    n_mels = 138
    fmin = 27.5
    fmax = 16000.
    max_size = 3

    # create mel spectro
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n_fft,
                                       hop_length=hop_length,
                                       fmin=fmin,
                                       fmax=fmax,
                                       n_mels=n_mels)

    # superflux
    odf_sf = librosa.onset.onset_strength(S=librosa.power_to_db(S, ref=np.max),
                                          sr=sr,
                                          hop_length=hop_length,
                                          lag=lag, max_size=max_size)

    onset_sf = librosa.onset.onset_detect(onset_envelope=odf_sf,
                                          sr=sr,
                                          hop_length=hop_length,
                                          units='time')
    return onset_sf * 1000


def debug(path):
    y, sr = librosa.load(path)

    # params
    n_fft = 1024
    hop_length = int(librosa.time_to_samples(1. / 200, sr=sr))
    lag = 2
    n_mels = 138
    fmin = 27.5
    fmax = 16000.
    max_size = 3

    # default
    odf_default = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)
    onset_default = librosa.onset.onset_detect(y=y, sr=sr, hop_length=hop_length,
                                               units='time')

    # create mel spectro
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n_fft,
                                       hop_length=hop_length,
                                       fmin=fmin,
                                       fmax=fmax,
                                       n_mels=n_mels)

    # superflux
    odf_sf = librosa.onset.onset_strength(S=librosa.power_to_db(S, ref=np.max),
                                          sr=sr,
                                          hop_length=hop_length,
                                          lag=lag, max_size=max_size)

    onset_sf = librosa.onset.onset_detect(onset_envelope=odf_sf,
                                          sr=sr,
                                          hop_length=hop_length,
                                          units='time')

    print(onset_sf * 1000)

    # display
    # sphinx_gallery_thumbnail_number = 2
    fig, ax = plt.subplots(nrows=3, sharex=True)

    frame_time = librosa.frames_to_time(np.arange(len(odf_default)),
                                        sr=sr,
                                        hop_length=hop_length)

    librosa.display.specshow(librosa.power_to_db(S, ref=np.max),
                             y_axis='mel', x_axis='time', sr=sr,
                             hop_length=hop_length, fmin=fmin, fmax=fmax, ax=ax[2])
    ax[2].set(xlim=[0, 15.0])

    ax[0].plot(frame_time, odf_default, label='Spectral flux')
    ax[0].vlines(onset_default, 0, odf_default.max(), color='r', label='Onsets')
    ax[0].legend()
    ax[0].label_outer()

    ax[1].plot(frame_time, odf_sf, color='g', label='Superflux')
    ax[1].vlines(onset_sf, 0, odf_sf.max(), color='r', label='Onsets')
    ax[1].legend()
    ax[0].label_outer()
    plt.show()
