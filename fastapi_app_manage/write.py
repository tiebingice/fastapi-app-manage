import pathlib
import typer


def write_router(name: str, is_utils: bool = False):
    if is_utils:
        return f"""
from fastapi_utils.cbv import cbv
from fastapi import APIRouter
router = APIRouter()

@cbv(router)
class {name.title()}View:

    @router.get("/")
    async def get(self):
        return
"""
    else:
        return f"""
from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def get():
    return
"""


def write_service(name: str):
    return f"""
from fastapi import Depends, HTTPException
class {name.title()}Service:
    def __init__(self):
        pass
"""


def write_schema():
    return """
from pydantic import BaseModel
    """


def write_lifespan(db_framwork: str = "tortoise-orm"):
    if db_framwork == "tortoise-orm":
        return """
from contextlib import asynccontextmanager
from fastapi import FastAPI
from tortoise.contrib.fastapi import RegisterTortoise
from settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with RegisterTortoise(
            app=app,
            config=settings.tortoise_config
    ):
        yield

        """
    else:
        return """
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app:FastAPI):
    print(1)
    yield
    print(2)

        """


def write_model(db_framwork: str):
    if db_framwork == "tortoise-orm":
        return """
from tortoise import fields
from tortoise.models import Model
    """
    else:
        return """
from sqlmodel import Field, SQLModel, create_engine
        """


def write_database():
    return """
from sqlmodel import Field, SQLModel, create_engine
from settings impirt settings
engine = create_engine(settings.db_url, echo=True)

    """


def write_main(cors: bool = False):
    if cors:
        return """
from fastapi import FastAPI
from app.core.lifespan import lifespan
from app.router import router
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI(
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

        """
    return """
from fastapi import FastAPI
from app.core.lifespan import lifespan
from app.router import router
app=FastAPI(
    lifespan=lifespan
)
    """


def write_settings(utils: bool = False, db_framework: str = "None"
                   ):
    if utils:
        if db_framework.title() == "None":
            return """
from fastapi_utils.api_settings import APISettings
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(APISettings):
     model_config = SettingsConfigDict(
            env_file=".env"
        )

settings=Settings()
        """
        elif db_framework == "tortoise-orm":
            return """
from fastapi_utils.api_settings import APISettings
from pydantic_settings import SettingsConfigDict

class Settings(APISettings):
    db_host: str = "localhost"
    db_port: int = 6379
    db_user: str = "root"
    db_password: str = "password"
    database: str = "database"

    model_config = SettingsConfigDict(
        env_file=".env"
    )

    @property
    def tortoise_config(self):
        return {
            'connections': {
                # Dict format for connection
                'default': {
                    'engine': 'tortoise.backends.',
                    'credentials': {
                        'host': self.db_host,
                        'port': self.db_port,
                        'user': self.db_user,
                        'password': self.db_password,
                        'database': self.database,
                    }
                },

            },
            'apps': {
                'models': {
                    'models': ['app.models'],
                    'default_connection': 'default',
                }
            }
        }
settings=Settings()

            """
        elif db_framework == "sqlmodel":
            return """
from fastapi_utils.api_settings import APISettings
from pydantic_settings import SettingsConfigDict

class Settings(APISettings):
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = "password"
    database: str = "your_database_name"

    model_config = SettingsConfigDict(
        env_file=".env"
    )

    @property
    def database_url(self):
        return f"  +  ://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.database}"

settings = Settings()

"""
    else:
        if db_framework.title() == "None":
            return """
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
     config = SettingsConfigDict(
            env_file=".env"
        )
settings=Settings()
"""
        elif db_framework == "tortoise-orm":
            return """
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 6379
    db_user: str = "root"
    db_password: str = "password"
    database: str = "database"

    model_config = SettingsConfigDict(
        env_file=".env"
    )

    @property
    def tortoise_config(self):
        return {
            'connections': {
                # Dict format for connection
                'default': {
                    'engine': 'tortoise.backends.',
                    'credentials': {
                        'host': self.db_host,
                        'port': self.db_port,
                        'user': self.db_user,
                        'password': self.db_password,
                        'database': self.database,
                    }
                },

            },
            'apps': {
                'models': {
                    'models': ['app.models'],
                    'default_connection': 'default',
                }
            }
        }


settings = Settings()

"""
        elif db_framework == "sqlmodel":
            return """
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = "password"
    database: str = "your_database_name"

    model_config = SettingsConfigDict(
        env_file=".env"
    )

    @property
    def database_url(self):
        return f"  +  ://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.database}"

settings = Settings()
            """


def write_router_init(name: str):
    return f"""
from fastapi import APIRouter
from .{name} import router as {name}_router
router = APIRouter()
"""


def write_router_init_(name: str):
    app_path = pathlib.Path("app")
    router_path = app_path / "router"
    router_path_init = router_path / "__init__.py"
    code = router_path_init.read_text()
    index = code.find("from fastapi import APIRouter")
    if index != -1:
        update_index = index + len("from fastapi import APIRouter")
        update_code = code[:update_index] + f"\nfrom .{name} import router as {name}_router" + code[update_index:]
        return update_code
    typer.echo("can not rewrite router __init___.py", err=True)
    return code


def write_result():
    return """
from pydantic import BaseModel
from typing import TypeVar, Generic

T = TypeVar('T')


class Result(BaseModel, Generic[T]):
    code: int = 200
    msg: str = 'success'
    data: T = None

    @classmethod
    def success(cls, code: int = 200, msg: str = "success", data: T = None) -> T:
        return cls(code=code, msg=msg, data=data)

    @classmethod
    def failure(cls, code: int = 400, msg: str = "failure", data: T = None) -> T:
        return cls(code=code, msg=msg, data=data)


    """
