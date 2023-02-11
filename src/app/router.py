from fastapi import APIRouter
from .library.album.endpoint.album_endpoint import album_router
from .library.artist.endpoint.artist_endpoint import artist_router
from .library.genre.endpoint.genre_endpoint import genre_router
from .library.playlist.endpoint.playlist_endpoint import playlist_router
from .library.track.endpoint.track_endpoint import track_router
from .library.endpoint.library_endpoint import library_router
from .user.endpoint.user_endpoint import user_router, comment_router

from . import router_schemas
from . import router_service


page_router = APIRouter(tags=['page'])


@page_router.get('/main', response_model=router_schemas.Main_page_get)
async def get_main_page(
    user_id: int
):
    return await router_service.main_s.get_main_page(id=user_id)

@page_router.get('/library', response_model=router_schemas.Library_page_get)
async def get_library_page(
    library_id: int
):
    return await router_service.main_s.get_library_page(id=library_id)

@page_router.get('/search', response_model=router_schemas.Search_page_get)
async def get_search_page():
    pass


api_router = APIRouter()

api_router.include_router(album_router, prefix='/album', tags=['album'])
api_router.include_router(artist_router, prefix='/artist', tags=['artist'])
api_router.include_router(genre_router, prefix='/genre', tags=['genre'])
api_router.include_router(playlist_router, prefix='/playlist', tags=['playlist'])
api_router.include_router(track_router, prefix='/track', tags=['track'])
api_router.include_router(library_router, prefix='/library', tags=['library'])
api_router.include_router(user_router, prefix='/user', tags=['user'])
api_router.include_router(comment_router, prefix='/comment', tags=['comment'])
api_router.include_router(page_router)