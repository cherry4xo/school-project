from typing import Optional, List

from fastapi import HTTPException
#from tortoise.query_utils import Query

from ..base.service_base import Service_base
from ..library import models
from ..library import schemas


class Library_service(Service_base):
    model = models.Library
    create_schema = schemas.Library_create
    get_schema = schemas.Library_get
    create_m2m_schema = schemas.Library_adds

    async def create(self, schema, user, **kwargs) -> Optional[schemas.Create]:
        obj = await self.model.create(schema.dict(exclude_unset=True), user_id=user.id, **kwargs)
        return await self.get_schema.from_tortoise_orm(obj)


library_s = Library_service()
