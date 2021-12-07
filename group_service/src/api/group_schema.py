from pydantic import BaseModel
from fastapi_utils.api_model import APIModel


class GroupIn(APIModel):
    user_id: int
    name: str
    description: str


class GroupOut(GroupIn):
    url: str


def response_model_error(status: int, detail: str):
    return {
        "status code": status,
        "detail": detail
    }
