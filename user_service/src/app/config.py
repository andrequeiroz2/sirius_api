import os
from functools import lru_cache
from pydantic import root_validator
from dotenv import find_dotenv, load_dotenv
from pydantic.env_settings import BaseSettings


load_dotenv(find_dotenv(filename=".env", raise_error_if_not_found=True))


def get_database_uri() -> str:
    username: str = os.getenv("USER_DB")
    password: str = os.getenv("PASSWORD_DB")
    host: str = os.getenv("DATABASE_HOST")
    port: int = int(os.getenv("DATABASE_PORT"))
    database_name: str = os.getenv("DATABASE_NAME")
    return f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}"



class Settings(BaseSettings):
    APP_NAME: str = os.getenv("APP_NAME")
    API_TITLE: str = os.getenv("API_TITLE")
    #SQLALCHEMY_DATABASE_URI: str = get_database_uri()

    @root_validator(pre=True)
    def validate_all(cls, values):
        for key, value in values.items():
            if any(
                (
                    value is None,
                    isinstance(value, str) and not value,
                    isinstance(value, str) and value.isspace(),
                )
            ):
                raise EnvironmentError(f"Erro in .env, verify the variable: {key}")
        return values
    
    class Config:
        case_sensitive = True


#@lru_cache
# def get_api_settings() -> Settings:
#     return Settings()
#
#
# settings = get_api_settings()
