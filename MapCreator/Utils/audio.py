import librosa.feature
import matplotlib.pyplot as plt
import numpy as np


def load_melspectrogram(audio_path, plot=False):
    y, sr = librosa.load(audio_path, sr=22050)
    melspectrogram = np.zeros((128, 20000), dtype=float)
    melspectrogram_full = librosa.feature.melspectrogram(y=y, sr=sr)
    melspectrogram[:, :melspectrogram_full.shape[1]] = melspectrogram_full[:, :20000]
    if plot:
        fig, ax = plt.subplots()
        S_dB = librosa.power_to_db(melspectrogram, ref=np.max)
        img = librosa.display.specshow(S_dB, x_axis='time',
                                       y_axis='mel', sr=sr, ax=ax)
        fig.colorbar(img, ax=ax, format='%+2.0f dB')
        ax.set(title='Mel-frequency spectrogram')
        plt.show()
    return melspectrogram.transpose()


if __name__ == "__main__":
    path = "C:/Users/Lysandre/Documents/GitHub/OsuMapCreator/MapCreator/datasets/maps/33688 DJ Okawari - Flower " \
           "Dance/Flower Dance.mp3"
    mel_spectro = load_melspectrogram(path, plot=True)

