import librosa
import matplotlib.pyplot as plt
import numpy as np
from numpy import ndarray


# def compute_beat_track(path) -> ndarray:
#     y, sr = librosa.load(path)
#     onset_env = librosa.onset.onset_strength(y=y, sr=sr)
#     tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env,
#                                            units='time')
#     return beats * 1000
#
#
# def compute_plp(path) -> ndarray:
#     y, sr = librosa.load(path)
#     onset_env = librosa.onset.onset_strength(y=y, sr=sr)
#     pulse = librosa.beat.plp(onset_envelope=onset_env, sr=sr)
#     times = librosa.times_like(pulse, sr=sr)
#     beats_plp = np.flatnonzero(librosa.util.localmax(pulse))
#     return times[beats_plp] * 1000
#
#
# def compute_plp_prior(path) -> ndarray:
#     y, sr = librosa.load(path)
#
#     import scipy.stats
#     onset_env = librosa.onset.onset_strength(y=y, sr=sr)
#     prior = scipy.stats.lognorm(loc=np.log(120), scale=120, s=1)
#     pulse_lognorm = librosa.beat.plp(onset_envelope=onset_env, sr=sr,
#                                      prior=prior)
#     times = librosa.times_like(pulse_lognorm, sr=sr)
#     beats_plp = np.flatnonzero(librosa.util.localmax(pulse_lognorm))
#     return times[beats_plp] * 1000
#
#
# def compute_onset_default(path) -> ndarray:
#     y, sr = librosa.load(path)
#
#     # params
#     hop_length = int(librosa.time_to_samples(1. / 200, sr=sr))
#
#     # default
#     # odf_default = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)
#     onset_default = librosa.onset.onset_detect(y=y, sr=sr, hop_length=hop_length,
#                                                units='time')
#
#     return onset_default * 1000


def compute_onset_superflux(y, sr) -> ndarray:
    # params
    n_fft = 1024
    hop_length = int(librosa.time_to_samples(1. / 200, sr=sr))
    lag = 2
    n_mels = 138
    fmin = 27.5
    fmax = 16000.
    max_size = 3
    # we don't need the first 5 seconds
    y = y[sr * 4:]

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


def load(audio):
    y, sr = librosa.load(audio)
    return y, sr


def compute_bpm(y, sr):
    onset_env = librosa.onset.onset_strength(y, sr=sr)
    tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)


# def compute_change_in_bpm(y, sr):
#     tempo, time = compute_local_bpm(y, sr)
#     beats = []
#     curr_bpm = 0
#     for i in range(len(tempo)):
#         if tempo[i] != curr_bpm:
#             curr_bpm = tempo[i]
#             beats.append([tempo[i], time[i]])
#     return beats


def tempo_(y, sr):
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    dtempo = librosa.feature.tempo(onset_envelope=onset_env, sr=sr,
                                   aggregate=None)
    return dtempo


def bpm(y, sr):
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    return tempo


def compute_local_bpm(y, sr):
    dtempo = tempo_(y, sr)
    tempo_time = librosa.times_like(dtempo, sr=sr) * 1000

    return [round(x) for x in dtempo], [round(x) for x in tempo_time]

# TODO create algo to center/tie the beatpoint time to the measure
