from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from typing_extensions import Annotated

from schemas import *
from crud import select_objects, update_objects, insert_objects, delete_objects


async def get_objects(serializer, offset: int = 0, limit: int = 10, order_by=None):
    _objects = await select_objects(serializer.Config.__table_name__,
                                   _limit=limit, _offset=offset,
                                   _order_by=order_by)
    objects = list()
    for i in _objects:
        objects.append(serializer.from_row(i).model_dump())
    return objects


async def get_object(serializer, id=None):
    pk_field = serializer.Config.__pk_field__
    if id is None:
        raise HTTPException(status_code=404, detail=f"{serializer.__name__} not found")
    _queryset = await select_objects(serializer.Config.__table_name__,
                                     **{pk_field: id})
    if not _queryset:
        raise HTTPException(status_code=404, detail=f"{serializer.__name__} not found")
    return serializer.from_row(_queryset[0]).model_dump()


async def update_object(instance: BaseModel):
    pk_field = instance.Config.__pk_field__
    if getattr(instance, pk_field) is None:
        raise HTTPException(status_code=404, detail=f"{instance.__class__.__name__} not found")

    fk_fields = instance.Config.__fk_fields__
    for f, s in fk_fields.items():
        if getattr(instance, f) is not None:
            existing = await get_object(s, getattr(instance, f))

    existing = await get_object(instance.__class__, getattr(instance, pk_field))
    await update_objects(instance.Config.__table_name__,
                         _set=instance.model_dump(exclude={pk_field}),
                         where={pk_field: getattr(instance, pk_field)}
                         )
    instance = await get_object(instance.__class__, getattr(instance, pk_field))
    return instance


async def create_object(instance: BaseModel):
    pk_field = instance.Config.__pk_field__
    fk_fields = instance.Config.__fk_fields__
    for f, s in fk_fields.items():
        if getattr(instance, f) is not None:
            existing = await get_object(s, getattr(instance, f))
    dump = instance.model_dump(exclude={pk_field})
    result = await insert_objects(instance.Config.__table_name__,
                                  tuple(dump.keys()),
                                  tuple(dump.values()),
                                  pk_field=pk_field)
    instance = await get_object(instance.__class__, result[0][pk_field])
    return instance


async def delete_object(serializer, id=None):
    pk_field = serializer.Config.__pk_field__
    if id is None:
        raise HTTPException(status_code=404, detail=f"{serializer.__name__} not found")
    result = await delete_objects(serializer.Config.__table_name__,
                                  pk_field=pk_field,
                                  **{pk_field: id},
                                  )
    if result:
        return result[0][pk_field]
    raise HTTPException(status_code=404, detail=f"{serializer.__name__} not found")
