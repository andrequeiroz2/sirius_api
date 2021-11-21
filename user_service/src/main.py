from fastapi import FastAPI
from uvicorn import run
from api.user_route import user_route
from app.db import Base, engine

Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI(openapi_url="/api/v1/user/openapi.json", docs_url="/api/v1/user/docs")

app.include_router(user_route, tags=['users'])


if __name__ == "__main__":
    run(app, host="127.0.0.1", port=7050, log_level="debug")
