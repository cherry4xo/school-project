from typing import Optional, List

from fastapi import HTTPException
#from tortoise.query_utils import Query

from ..base.service_base import Service_base
from ..library import models
from ..library import schemas


class Library_service(Service_base):
    model = models.Library
    create_schema = schemas.Library_create
    get_schema = schemas.Library_get_schema
    create_m2m_schema = schemas.Library_adds

    async def create(self, user_id, **kwargs) -> Optional[schemas.Create]:
        _user = await models.User.get_or_none(id=user_id)
        if not _user:
            raise HTTPException(status_code=404, detail=f'User {user_id} does not exist')
        obj = await self.model.create(user_id=_user.id, **kwargs)
        return await self.get_schema.from_tortoise_orm(obj)

    async def get_user_id(self, id, **kwargs) -> Optional[schemas.Library_get]:
        _library = await self.model.get_or_none(id=id)
        if not _library:
            raise HTTPException(status_code=404, detail=f'Library {id} does not exist')
        user_id = await models.User.filter(id=_library.user).first().values('id')
        return user_id

    async def get(self, id, **kwargs):
        library = await self.model.get_or_none(id=id)
        if not library:
            raise HTTPException(status_code=404, detail=f'Library {id} does not exist')
        user = await models.User.get(id=library.user_id)
        response = {'id': library.id, 'user_id': {'id': user.id}}
        return response


library_s = Library_service()
