from fastapi import FastAPI
from uvicorn import run
from api.group_route import group_route
from app.db import client

app: FastAPI = FastAPI(
    openapi_url="/api/v1/group/openapi.json",
    docs_url="/api/v1/group/docs"
)

app.include_router(group_route, tags=['group'])


if __name__ == "__main__":
    run(app, host="127.0.0.1", port=7060, log_level="debug")
