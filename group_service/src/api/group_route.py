from fastapi import APIRouter, status
from .group_schema import GroupIn, GroupOut
from .group_schema import response_model_error
from .group_controller import (
    get_groups,
    create_group,
    get_group,
    count_collection,
    count_group
)

group_route = APIRouter()


@group_route.get("/groups/")
async def get_list_group(skip: int = 0, limit: int = 50) -> list[GroupOut]:
    db_group = await get_groups(skip=skip, limit=limit)
    if not db_group:
        return response_model_error(
            status=status.HTTP_404_NOT_FOUND,
            detail="groups not found"
        )
    return db_group


@group_route.get("/groups/count")
async def get_count_total() -> int:
    return await count_collection()


@group_route.get("/groups/{user_id}")
async def get(user_id: int) -> GroupOut:
    db_group = await get_group(user_id=user_id)
    if not db_group:
        return response_model_error(
            status=status.HTTP_404_NOT_FOUND,
            detail="group not found"
        )
    return await get_group(user_id=user_id)


@group_route.get("/groups/count/{user_id}")
async def get_list(user_id: int) -> int:
    return await count_group(user_id=user_id)


@group_route.put("/groups/", status_code=status.HTTP_202_ACCEPTED)
async def put(group: GroupIn):
    await create_group(group=group)
    return {"msg": "success"}
