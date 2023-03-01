from typing import List
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from tortoise.contrib.fastapi import HTTPNotFoundError, JSONResponse
from .. import schemas
from .. import models
from .. import service


user_router = APIRouter()
comment_router = APIRouter()
templates = Jinja2Templates(directory='templates')


def artists_checker(artists: List[str] = Form(None)):
    if len(artists) == 1:
        artists = [item.strip() for item in artists[0].split(',')]

    return [artist for artist in artists]

def genres_checker(genres: List[str] = Form(None)):
    if len(genres) == 1:
        genres = [item.strip() for item in genres[0].split(',')]

    return [genre for genre in genres]


@user_router.post('/create', status_code=status.HTTP_200_OK)
async def user_create(
    user: schemas.User_create_request = Depends(schemas.User_create_request.as_form),
    artists: List[int] = Depends(artists_checker),
    genres: List[int] = Depends(genres_checker),
    picture_file: UploadFile = File(...)
):
    return await service.user_s.create(user, artists, genres, picture_file)

@user_router.put('/change/data/{user_id}', response_model=schemas.User_change_picture_response)
async def user_change_picture(
    user_id: int = Depends(schemas.User_change_picture.as_form),
    new_picture_file: UploadFile = File(...),
):
    return await service.user_s.change_picture(user_id, new_picture_file)

@user_router.delete('/delete/data/{user_id}', status_code=204)
async def user_delete_picture(
    user_id: int = Depends(schemas.User_change_picture.as_form) 
):
    return await service.user_s.delete_picture(user_id)

@user_router.get('/get_picture/{user_id}', response_class=FileResponse)
async def user_get_picture(
    user_id: int
):
    return await service.user_s.get_image(id=user_id)

@user_router.get('/{user_id}', response_model=schemas.User_get)
async def user_get(
    user_id: int
):
    return await service.user_s.get(id=user_id)

@user_router.put('/update', response_model=schemas.User)
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

@user_router.put('/', status_code=204)
async def user_change_password(
    user_id: int,
    old_password: str,
    new_password: str
):
    return await service.user_s.change_password(old_password=old_password, new_password=new_password, id=user_id)

'''@user_router.get('/get_obj/{user_id}', response_model=schemas.getUser)
async def user_get_obj(
    user_id: int
):
    return await service.user_s.get_obj(id=user_id)'''

@comment_router.post('/', response_model=schemas.Comment_get)
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

@comment_router.put('/', response_model=schemas.Comment_update)
async def comment_update(
    comment_id: int,
    comment: schemas.Comment_update,
):
    return await service.comment_s.update(comment, id=comment_id)

@comment_router.delete('/', status_code=204)
async def comment_delete(
    comment_id: int
):
    return await service.comment_s.delete(id=comment_id)

@comment_router.get('/', response_model=schemas.Comment_get)
async def comment_get(
    comment_id: int
):
    return await service.comment_s.get(id=comment_id)