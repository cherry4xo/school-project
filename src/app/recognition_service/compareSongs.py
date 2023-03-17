from fingerprint import fingerprintSeparate

# Choose your audioFiles
fileName1 = "Rammstein_-_DEUTSCHLAND_(musmore.com).mp3" # file pathes for testing
fileName2 = "audio_2023-03-10_16-15-22.mp3"

class Recognition_algorithm:
    def comparePeaks(self, peaks1, peaks2):
        dif = []
        callback = 0
        for i in range(len(peaks1)):
            dif.append((peaks2[i] - peaks1[i])**2)

        for i in dif:
            callback+=i

        return callback

    def compareSongs(self, fileName1, fileName2):
        fingerprint1 = fingerprintSeparate(fileName1, plot=False) # full song
        fingerprint2 = fingerprintSeparate(fileName2, plot=False) # recorded audio

        step = len(fingerprint2)

        compares = []

        for i in range(len(fingerprint2), len(fingerprint1)):
            peaks1 = fingerprint1[i-step:i]
            comparison = self.comparePeaks(peaks1, fingerprint2)
            compares.append(comparison)

        return min(compares)

recog_algo = Recognition_algorithm()

'''def comparePeaks(peaks1, peaks2):
    dif = []
    callback = 0
    for i in range(len(peaks1)):
        dif.append((peaks2[i] - peaks1[i])**2)

    for i in dif:
        callback+=i

    return callback


def compareSongs(fileName1, fileName2):
    fingerprint1 = fingerprintSeparate(fileName1, plot=False) # full song
    fingerprint2 = fingerprintSeparate(fileName2, plot=False) # recorded audio

    step = len(fingerprint2)

    compares = []

    for i in range(len(fingerprint2), len(fingerprint1)):
        peaks1 = fingerprint1[i-step:i]
        comparison = comparePeaks(peaks1, fingerprint2)
        compares.append(comparison)

    return min(compares)

ans = compareSongs(fileName1, fileName2)

print(ans)'''
