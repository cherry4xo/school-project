import pydub
import os
from pathlib import Path

def convertMP3ToWav(fileName):
    #os.chmod(rf'{fileName}', 777)
    #file_path = Path(os.getcwd().__str__() + '\\' + fileName)
    sound = pydub.AudioSegment.from_mp3(rf'{fileName}')
    #sound.export("last_recorded_audio.wav", format="wav")
    return sound

def convertMP3ToWavForUpload(fileName):
    sound = pydub.AudioSegment.from_mp3(rf'{fileName}')
    sound.export('src/app/recognition_service/data/last_recorded_audio.wav', format="wav")