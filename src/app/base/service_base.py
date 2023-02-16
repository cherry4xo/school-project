from typing import TypeVar, Type, Optional, List

from fastapi import HTTPException
from pydantic import BaseModel
from tortoise import models
from tortoise.models import Model


Model_type = TypeVar('Model_type', bound=models.Model)
Create_schema_type = TypeVar('Create_schema_type', bound=BaseModel)
Create_m2m_schema_type = TypeVar('Create_m2m_schema_type', bound=BaseModel)
Update_schema_type = TypeVar('Update_schema_type', bound=BaseModel)
Get_schema_type = TypeVar('Get_schema_type', bound=BaseModel)
Query_schema_type = TypeVar('Query_schema_type', bound=BaseModel)


class Service_base:
    model: Type[Model_type]
    create_schema: Type[Create_schema_type]
    create_m2m_schema: Type[Create_m2m_schema_type]
    update_schema: Type[Update_schema_type]
    query_scheme: Type[Query_schema_type]
    get_schema: Type[Get_schema_type]

    async def create(self, schema, *args, **kwargs) -> Optional[Create_schema_type]:
        obj = await self.model.create(**schema.dict(exclude_unset=True), **kwargs)
        return await self.get_schema.from_tortoise_orm(obj)

    async def update(self, schema, **kwargs) -> Optional[Update_schema_type]:
        await self.model.filter(**kwargs).update(**schema.dict(exclude_unset=True))
        return await self.get_schema.from_queryset_single(self.model.get(**kwargs))

    async def delete(self, **kwargs):
        obj = await self.model.filter(**kwargs).delete()
        if not obj: 
            raise HTTPException(status_code=404, detail='Object does not exist')

    async def all(self) -> Optional[Get_schema_type]:
        return await self.get_schema.from_queryset(self.model.all())

    async def filter(self, **kwargs) -> Optional[Get_schema_type]:
        return await self.get_schema.from_queryset(self.model.filter(**kwargs))

    async def get(self, **kwargs) -> Optional[Get_schema_type]:
        return await self.get_schema.from_queryset_single(self.model.get(**kwargs))

    async def get_obj(self, **kwargs) -> Optional[Model_type]:
        return await self.model.get_or_none(**kwargs)

    async def create_m2m(self, *args, **kwargs) -> Optional[Create_m2m_schema_type]:
        obj = await self.model.filter(**kwargs).delete()
        if not obj:
            raise HTTPException(status=404, detail='Object does not exist')
        _adds = await models.Adds_model.filter(id=args)
        await obj.adds.add(*_adds)
        return await self.get_schema.from_tortoise_orm(obj)

    async def add_m2m_fields(self, obj_id: int, adds_ids: List[int]):
        obj = await self.model.get_or_none(id=obj_id)
        if not obj:
            raise HTTPException(status_code=404, detail=f'Library {id} does not exist')
        _adds_list = await models.Track.filter(id__in=adds_ids)
        await obj.tracks.add(*_adds_list)

    async def remove_m2m_fields(self, adds_model: Model, parts_model, obj_id: int, adds_ids: List[int]):
        obj = await self.model.get_or_none(id=obj_id)
        if not obj:
            raise HTTPException(status_code=404, detail=f'Library {id} does not exist')
        _adds_list = await adds_model.filter(id__in=adds_ids)
        await obj.parts_model.remove(*_adds_list)