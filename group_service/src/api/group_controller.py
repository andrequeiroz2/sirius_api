from .group_schema import GroupOut, GroupIn
from app.db import group_collection, db


async def get_groups(skip: int = 0, limit: int = 50) -> list[GroupOut]:
    group_model_list: list[GroupOut] = list(group_collection.find({}, {'_id': False}))
    return group_model_list


async def get_group(user_id: int) -> GroupOut:
    return group_collection.find({"user_id": user_id}, {'_id': False})


async def create_group(group: GroupIn) -> GroupOut:
    return db.groups.insert_one(dict(group)).inserted_id


async def count_collection() -> int:
    return group_collection.count_documents({})


async def count_group(user_id: int) -> int:
    return group_collection.count_documents({"user_id": user_id})
