import os
import json
import uuid
import shutil

from typing import Optional, List
from collections import defaultdict

import numpy as np

from fastapi import HTTPException, Form, Depends, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.concurrency import run_in_threadpool

from .fingerprint import fingerprintSeparate
from . import convert
from ..base.service_base import Service_base
from .. library import models
from . import models as model_spectro
from . import schemas


class Recognition_service(Service_base):
    model = model_spectro.Track_spectorgram
    get_schema = schemas.Get_track_spectrogram

    async def upload_last_recorded_audio_file(self, file: UploadFile = File(...)):
        try:
            file_directory = 'src/app/recognition_service/data'
            if not os.path.exists(file_directory):
                os.makedirs(file_directory)
            file.filename = 'last_recorded_audio.mp3'
            f = await run_in_threadpool(open, f'{file_directory}/{file.filename}', 'wb')
            await run_in_threadpool(shutil.copyfileobj, file.file, f)
            await run_in_threadpool(convert.convertMP3ToWavForUpload, f'{file_directory}/last_recorded_audio.wav', format='wav')
            await run_in_threadpool(os.remove, 'src/app/recognition_service/data/last_recorded_audio.mp3')
        except Exception():
            return {'file_path': 'NULL'}
        finally:
            if 'f' in locals(): await run_in_threadpool(f.close)
            await file.close()

    async def create(self, track_id: int) -> Optional[None]:
        obj = await models.Track.get(id=track_id)
        spectro = await model_spectro.Track_spectorgram.create(track_id=obj)
        await spectro.save()
        await self.make_peaks_file_from_list(track_id=track_id)

    async def make_peaks_file_from_list(self, track_id: int) -> Optional[None]:
        obj = await models.Track.get(id=track_id)
        obj_spectro = await model_spectro.Track_spectorgram.get(track_id=obj)
        print(obj.track_file_path)
        peaks = fingerprintSeparate(obj.track_file_path)
        file_dir = 'data/spectrograms'
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        filename = f'{str(uuid.uuid4())}.csv'
        if obj_spectro.peaks_file_path:
            os.remove(obj_spectro.peaks_file_path)
            obj_spectro.peaks_file_path = None
            obj_spectro.update(peaks_file_path=None)
        np.savetxt(filename, peaks, delimiter=',', fmt='% s')
        obj_spectro.update(peaks_file_path=filename)

    async def delete_track_spectrogram_file(self, track_id: int) -> Optional[None]:
        track_spectro = await model_spectro.get(track_id_id=track_id)
        if track_spectro.peaks_file_path:
            os.remove(track_spectro.peaks_file_path)
            track_spectro.peaks_file_path = None
            track_spectro.update(peaks_file_path=None)

    async def get_peaks_list_from_file(self, track_id: int) -> Optional[List]:
        obj = await model_spectro.Track_spectorgram.get(track_id_id=track_id)
        peaks = np.loadtxt(obj.spectorgram_file_path, delimiter=',', dtype=int)
        peaks_list = peaks.tolist()
        return peaks_list 

    async def get_min_compares_from_tracks(self, library_id: int = Form(...), recorded_file: UploadFile = File(...)) -> Optional[schemas.Track_page_get]:
        last_recorded_audio_path = 'src/app/recognition_service/data/last_recorded_audio.wav'
        if os.path.isfile(last_recorded_audio_path):
            os.remove(last_recorded_audio_path)
        await self.upload_file(recorded_file)
        track_ids = await models.Track.all().values('id')
        track_compares = [(await self.compareSongs(track_id)).keys() for track_id in track_ids]
        track_compares = list(map(int, track_compares))
        request_track_id = max(track_compares)
        _track = await models.Track.get_or_none(id=request_track_id)
        _is_library_added = (await self.get_is_track_added(library_id=library_id, track_id=_track.id))['added']
        _artists_track = await models.Artist.filter(tracks=_track.id).values('id')
        _artists_track_response = []
        for j in _artists_track:
            _artist_track = await models.Artist.get(id=j['id'])
            _artists_track_response.append({'id': _artist_track.id, 
                                            'name': _artist_track.name})
        return {'track_data': await schemas.Track_pydantic.from_tortoise_orm(_track),
                'artists': _artists_track_response,
                'added': _is_library_added}

    async def comparePeaks(self, peaks1, peaks2) -> Optional[int]:
        dif = []
        callback = 0
        for i in range(len(peaks1)):
            dif.append((peaks2[i] - peaks1[i])**2)

        for i in dif:
            callback+=i

        return callback

    async def compareSongs(self, track_id: int) -> Optional[dict]:
        fingerprint1 = self.get_peaks_list_from_file(track_id=track_id) # track peaks from db
        fingerprint2 = fingerprintSeparate('last_recorded_audio.wav', plot=False) # recorded audio

        step = len(fingerprint2)

        compares = []

        for i in range(len(fingerprint2), len(fingerprint1)):
            peaks1 = fingerprint1[i-step:i]
            comparison = await self.comparePeaks(peaks1, fingerprint2)
            compares.append(comparison)

        return {f'{track_id}': min(compares)}


recog_s = Recognition_service()