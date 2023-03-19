from typing import List

from fastapi import APIRouter, HTTPException
from fastapi import HTTPException, Form, Depends, File, UploadFile
from tortoise.contrib.fastapi import HTTPNotFoundError

from . import schemas
from . import service
from . import models


recognition_router = APIRouter()


@recognition_router.post('/create', status_code=204)
async def create_track_spectrogram(
    track_id: int
):
    return await service.recog_s.create(track_id=track_id)

@recognition_router.delete('/delete', status_code=204)
async def delete_track_spectrorgam(
    track_id: int
):
    return await service.recog_s.delete(track_id=track_id)

@recognition_router.post('/make_peaks_file', status_code=204)
async def make_peaks_file(
    track_id: int
):
    return await service.recog_s.make_peaks_file_from_list(track_id=track_id)

@recognition_router.post('/delete_peaks_file', status_code=204)
async def delete_peaks_file(
    track_id: int
):
    return await service.recog_s.delete_track_spectrogram_file(track_id=track_id)

@recognition_router.post('/get_peaks_from_file', response_model=List)
async def get_peaks_from_file(
    track_id: int
):
    return await service.recog_s.get_peaks_list_from_file(track_id=track_id)

@recognition_router.post('/get_track_by_recorded_audio', response_model=schemas.Track_page_get)
async def get_track_by_recorded_audio(
    library_id: int = Form(...),
    recorded_file: UploadFile = File(...)
):
    return await service.recog_s.get_min_compares_from_tracks(library_id=library_id, recorded_file=recorded_file)

