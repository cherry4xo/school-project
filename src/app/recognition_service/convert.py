from pydub import AudioSegment

def convertMP3ToWav(fileName):
    AudioSegment.ffmpeg = 'data/track/track_file/'
    sound = AudioSegment.from_mp3(fileName)
    sound.export("last_recorded_audio.wav", format="wav")
    return sound

def convertMP3ToWavForUpload(fileName):
    AudioSegment.ffmpeg = 'src/app/recognition_service/data/'
    sound = AudioSegment.from_mp3(fileName)
    sound.export("last_recorded_audio.wav", format="wav")
    return sound