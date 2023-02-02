from typing import List
from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError, JSONResponse
from .. import schemas
from .. import models
from .. import service



user_router = APIRouter()
comment_router = APIRouter()


@user_router.post('/', response_model=schemas.User_get)
async def user_create(
    user: schemas.User_create, 
    genres: List[int],
    artists: List[int] 
):
    return await service.user_s.create(user, genres, artists)

@user_router.get('/{user_id}', response_model=schemas.User_get)
async def user_get(
    user_id: int
):
    return await service.user_s.get(id=user_id)

@user_router.put('/update', response_model=schemas.User_get)
async def user_update(
    user_id: int,
    user: schemas.User_update
):
    return await service.user_s.update(user, id=user_id)

@user_router.delete('/delete/{user_id}', status_code=204)
async def user_delete(
    user_id: int
):
    return await service.user_s.delete(id=user_id)

'''@user_router.get('/get_obj/{user_id}', response_model=schemas.getUser)
async def user_get_obj(
    user_id: int
):
    return await service.user_s.get_obj(id=user_id)'''

@comment_router.post('/ ', response_model=schemas.Comment_get)
async def comment_create(
    comment: schemas.Comment_create,
    user: int,
    track: int
):
    return await service.comment_s.create(comment, track, user)

@comment_router.get('/', response_model=schemas.Comment_get)
async def comment_get(
    comment_id: int
):
    return await service.comment_s.get(id=comment_id)

@comment_router.put('/', response_model=schemas.Comment_get)
async def comment_update(
    comment_id: int,
    comment: schemas.Comment_update,
):
    return await service.comment_s.update(comment, id=comment_id)

@comment_router.delete('/', response_model=schemas.Comment_delete)
async def comment_delete(
    comment_id: int
):
    return await service.comment_s.delete(id=comment_id)

@comment_router.get('/', response_model=List[schemas.Comment_get])
async def comment_filter_by_id(
    comments_id: List[int]
):
    return await service.comment_s.filter(id=comments_id)