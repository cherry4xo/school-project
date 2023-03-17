import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import sklearn
from scipy import signal
from spectromap.spectromap import peak_search
from .convert import convertMP3ToWav


def f_high(y, sr):
    b, a = signal.butter(10, 2000 / (sr / 2), btype='highpass')
    yf = signal.lfilter(b, a, y)
    return yf


def fingerprint(signal, sr, plot=False):

    signal_filtered = f_high(signal,sr)

    S = librosa.feature.melspectrogram(y=signal_filtered, sr=sr, n_fft=2048)

    spec = sklearn.preprocessing.normalize(S)


    S_dB = librosa.power_to_db(spec, ref=np.max)

    if (plot):
        librosa.display.specshow(S_dB, x_axis='time',
                                 y_axis='mel',
                                 sr=sr,
                                 fmax=10000)
        plt.plot()
        plt.show()

    fraction = 0.5  # Fraction of spectrogram to compute local comparisons
    condition = 2  # Axis to analyze (0: Time, 1: Frequency, 2: Time+Frequency)
    id_peaks, peaks = peak_search(spec, fraction, condition)

    # rounded_peaks = np.ndarray.round(peaks, 5)

    return spec, peaks[id_peaks]


def fingerprintSeparate(filename, plot=False):
    songPeaks = []

    secondSounds = []

    sound = convertMP3ToWav(filename) # change to audio from db

    for i in range(1000, len(sound), 1000):
        secondSounds.append(sound[i-1000:i])

    for i in range(len(secondSounds)):
        s = secondSounds[i]
        s.export("wavSound.wav", format="wav")
        signal, sr = librosa.load("wavSound.wav")

        # duration = librosa.get_duration(y=signal, sr=sr)
        # print(duration)

        spec, peaks = fingerprint(signal, sr)
        for peak in peaks:
            songPeaks.append(peak)

    if plot:
        plt.plot(songPeaks, '.k')
        plt.show()

    return songPeaks
