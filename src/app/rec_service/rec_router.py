from typing import List
from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError

from . import schemas
from . import service
from . import models

rec_router = APIRouter()

@rec_router.get('/get_recs_by_library_tracks')
async def get_recs_by_library_tracks(
    user_id: int
):
    return await service.rec_service.get_recommends_by_library_tracks(id=user_id)