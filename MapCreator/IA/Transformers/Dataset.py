import tensorflow as tf
import numpy as np
from MapCreator.Utils.trainingMapParser import load_beatmap_attributes
from pydub import AudioSegment


def flatten(l):
    flat_list = []
    for sublist in l:
        if type(sublist) == list:
            for item in sublist:
                flat_list.append(item)
        else:
            flat_list.append(sublist)
    return flat_list


def prepare_dataset(data, segment_length=5529, max_hitObject=120):
    end_of_sequence = 10002
    start_of_sequence = 10001
    music_segments = []  # List to store the split segments
    diff_segments = []  # List to store the split segments
    for beatmap in data:
        print(beatmap["audio"])
        # spectrogram using stft
        if beatmap["audio"].endswith(".mp3"):
            # convert mp3 to wav
            sound = AudioSegment.from_mp3(beatmap["audio"])
            beatmap["audio"] = beatmap["audio"][:-4] + ".wav"
            sound.export(beatmap["audio"], format="wav")
        audio = tf.io.read_file(beatmap["audio"])
        audio, _ = tf.audio.decode_wav(audio, 1)
        audio = tf.squeeze(audio, axis=-1)
        stfts = tf.signal.stft(audio, frame_length=200, frame_step=80, fft_length=256)
        x = tf.math.pow(tf.abs(stfts), 0.5)
        # normalisation
        means = tf.math.reduce_mean(x, 1, keepdims=True)
        stddevs = tf.math.reduce_std(x, 1, keepdims=True)
        x = (x - means) / stddevs
        audio_len = tf.shape(x)[0]
        # slicing to 10 seconds
        num_segments = int(np.ceil(audio_len / segment_length))

        for i in range(num_segments):
            start_sample = i * segment_length
            end_sample = start_sample + segment_length

            # Split the spectrogram and add the segment to the list
            segment = x[start_sample:end_sample, :]

            # Pad the last segment if necessary
            if tf.shape(segment)[0] < segment_length:
                paddings = tf.constant([[0, segment_length], [0, 0]])
                segment = tf.pad(segment, paddings, "CONSTANT")[:segment_length, :]

            music_segments.append(segment)

        # Slicing of the diff
        hitpoints = beatmap["text"]
        segment = [start_of_sequence]
        segment_id = 1
        for hitpoint in hitpoints:
            if hitpoint[4] >= 10000:
                print("Spinner ignoré :" + str(hitpoint[4]))
                continue
            # TODO : change 10000 in function of segment_length
            if 10000 * segment_id > hitpoint[2]:
                hitpoint[2] -= 10000 * (segment_id - 1)
                segment.append(hitpoint.tolist())
            else:
                for i in range(int(hitpoint[2] / 10000)-(segment_id-1)):
                    segment.append(end_of_sequence)
                    segment = flatten(segment)

                    # Padding the segment
                    segment += [0] * (max_hitObject*13 - len(segment))
                    if len(segment) > max_hitObject*13:
                        print("Warning : the length of the sequence exceeds the fixed limit")
                    diff_segments.append(segment)
                    segment = [start_of_sequence]
                    segment_id += 1
                hitpoint[2] -= 10000 * (segment_id - 1)
                segment.append(hitpoint.tolist())
        """if len(diff_segments[-1]) != max_hitObject*13:
            print("Ajustement")
            diff_segments[-1].append(end_of_sequence)
            diff_segments[-1] += [0] * (max_hitObject*13 - len(diff_segments[-1]) - 1)
            print(len(diff_segments[-1]))"""

        for i in range(num_segments - segment_id+1):
            diff_segments.append([start_of_sequence, end_of_sequence] + [0] * (max_hitObject*13 - 2))

    return music_segments, diff_segments


def create_text_and_audio_ds(data, bs=4):
    music_segments, diff_segments = prepare_dataset(data)
    print("Number of diff segments : " + str(len(diff_segments)))
    print("Number of music segments : " + str(len(music_segments)))
    audio_ds = tf.data.Dataset.from_tensor_slices(music_segments)
    map_ds = tf.data.Dataset.from_tensor_slices(diff_segments)
    ds = tf.data.Dataset.zip((audio_ds, map_ds))
    ds = ds.map(lambda x, y: {"source": x, "target": y})
    ds = ds.batch(bs)
    ds = ds.prefetch(tf.data.AUTOTUNE)
    return ds


def load_beatmaps_and_musics(paths, max_nb_musics=1000):
    data = []
    diff = []
    for i, path in enumerate(paths):
        if max_nb_musics and i >= max_nb_musics:
            break
        for beatmap in path[0]:
            df_temp, difficulty = load_beatmap_attributes(beatmap, max_hit_object=None)
            df_temp = df_temp.transpose()
            diff.append(difficulty)
            data.append({"audio": path[1], "text": df_temp})
    return data
