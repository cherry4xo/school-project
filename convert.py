from pydub import AudioSegment


def convertMP3ToWav(fileName):
    sound = AudioSegment.from_mp3(fileName)
    return sound
    # soundPart.export("wavSound.wav", format="wav")
