import pathlib
import typer

py_api_router_code = """
from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def get():
    return
"""

py_api_router_cbv_code = """
from fastapi_utils.cbv import cbv
from fastapi import APIRouter
router = APIRouter()

@cbv(router)
class {}View:

    @router.get("/")
    async def get(self):
        return
"""
py_service_code = """
from fastapi import Depends, HTTPException
class {}Service:
    def __init__(self):
        pass
"""

py_schema_code = """
from pydantic import BaseModel
"""

py_lifespan_code = """
from contextlib import asynccontextmanager
from fastapi import FastAPI
from tortoise.contrib.fastapi import RegisterTortoise
from settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    #1
        yield

"""

py_tortoise_orm_code = """
from tortoise import fields
from tortoise.models import Model
"""
py_sqlmodel_code = """
from sqlmodel import Field, SQLModel, create_engine
"""

py_core_db = """
from sqlmodel import Field, SQLModel, create_engine
from settings import settings
engine = create_engine(settings.db_url, echo=True)
"""

py_cors_fastapi_code = """
from fastapi import FastAPI
from app.core.lifespan import lifespan
from app.router import router
#2

app = FastAPI(
    lifespan=lifespan
)

#1
"""
py_pydantic_settings_code = """
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env"
    )
    #2
    #1

"""

py_pydantic_settings_code_ = """
from fastapi_utils.api_settings import APISettings
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(APISettings):
    model_config = SettingsConfigDict(
        env_file=".env"
    )
    #2
    #1


settings = Settings()
"""

py_router_init_code = """
from fastapi import APIRouter
from .{name} import router as {name}_router
router = APIRouter()
"""

py_standard_response_code = """
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

index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FastAPI App</title>
</head>
<body>
    <h1>Welcome to FastAPI App</h1>
    <p>This is a simple FastAPI application.</p>
</body>
</html>


"""


def write_html():
    return index_html


def write_router(name: str, is_utils: bool = False):
    if is_utils:
        return py_api_router_cbv_code.format(name.title())
    else:
        return py_api_router_code


def write_service(name: str):
    return py_service_code.format(name.title())


def write_schema():
    return py_schema_code


def write_lifespan(db_framwork: str = "tortoise-orm"):
    if db_framwork == "tortoise-orm":
        return py_lifespan_code.replace(
            "#1", """async with RegisterTortoise(
        app=app,
        config=settings.tortoise_config
    ): """

        )
    else:
        return py_lifespan_code.replace(
            "[1]", ""
        )


def write_model(db_framwork: str):
    if db_framwork == "tortoise-orm":
        return py_tortoise_orm_code
    else:
        return py_sqlmodel_code


def write_database():
    return py_core_db


def write_main(cors: bool = False):
    if cors:
        return py_cors_fastapi_code.replace(
            "#1", """app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
           """).replace(
            "#2", "from fastapi.middleware.cors import CORSMiddleware"
        )
    else:
        return py_cors_fastapi_code.replace("#1", "").replace("#2", "")


def write_settings(utils: bool = False, db_framework: str = "None"
                   ):
    code = py_pydantic_settings_code
    if utils:
        code = py_pydantic_settings_code_

    if db_framework.title() == "None":
        return code.replace("#1", "")

    elif db_framework == "tortoise-orm":
        return code.replace("#1", """@property
    def tortoise_config(self):
        return {
            'connections': {
                # Dict format for connection
                'default': {
                    'engine': 'tortoise.backends.mysql', #note: Replace according to the used database version, here we do not directly write the corresponding driver.
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

        """).replace(
            "#2", """db_host:str="127.0.0.1"
    db_port:int=6379
    db_user:str="root"
    db_password:str="pwd"
    database:str="db"
            """
        )
    else:
        return code.replace("#1", """@property
    def database_url(self):
        return f"pymysql+mysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.database}" # #note: Replace according to the used database version, here we do not directly write the corresponding driver.
        """).replace(
            "#2", """db_host:str="127.0.0.1"
    db_port:int=6379
    db_user:str="root"
    db_password:str="pwd"
    database:str="db"
            
            """
        )


def write_router_init(name: str):
    return py_router_init_code.format(name=name)


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
    return py_standard_response_code
