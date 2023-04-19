import librosa
import matplotlib.pyplot as plt
import numpy as np
from numpy import ndarray


def compute_beat_track(path) -> ndarray:
    y, sr = librosa.load(path)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env,
                                           units='time')
    return beats * 1000


def compute_plp(path) -> ndarray:
    y, sr = librosa.load(path)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    pulse = librosa.beat.plp(onset_envelope=onset_env, sr=sr)
    times = librosa.times_like(pulse, sr=sr)
    beats_plp = np.flatnonzero(librosa.util.localmax(pulse))
    return times[beats_plp] * 1000


def compute_plp_prior(path) -> ndarray:
    y, sr = librosa.load(path)

    import scipy.stats
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    prior = scipy.stats.lognorm(loc=np.log(120), scale=120, s=1)
    pulse_lognorm = librosa.beat.plp(onset_envelope=onset_env, sr=sr,
                                     prior=prior)
    times = librosa.times_like(pulse_lognorm, sr=sr)
    beats_plp = np.flatnonzero(librosa.util.localmax(pulse_lognorm))
    return times[beats_plp] * 1000


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


def compute_change_in_bpm(path):
    dtempo, time = compute_local_bpm(path)
    beats = []
    curr_bpm = 0
    for i in range(len(dtempo)):
        if dtempo[i] != curr_bpm:
            curr_bpm = dtempo[i]
            beats.append([dtempo[i], time[i]])
    return beats


def compute_local_bpm(path):
    y, sr = librosa.load(path)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    dtempo = librosa.feature.tempo(onset_envelope=onset_env, sr=sr,
                                   aggregate=None)
    dtempo_time = librosa.times_like(dtempo, sr=sr) * 1000

    return [round(x) for x in dtempo], [round(x) for x in dtempo_time]


# TODO create algo to center/tie the beatpoint time to the measure
def correct_time(path):
    beats = compute_change_in_bpm(path)
    bpm = 0
    pass


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
