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
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from settings import settings
from fastapi import Depends
from typing import Annotated


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_async_session():
    async with async_session_maker() as session:
        yield session
       

AsyncDBSession = Annotated[AsyncSession, Depends(get_async_session)]
 
"""

py_cors_fastapi_code = """
from fastapi import FastAPI
from app.core.lifespan import lifespan
from app.router import router
#2
#4

app = FastAPI(
    lifespan=lifespan,
    #3
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
from typing import TypeVar, Generic,Self

T = TypeVar('T')


class Result(BaseModel, Generic[T]):
    code: int = 200
    msg: str = 'success'
    data: T = None #type: ignore[assignment]

    @classmethod
    def success(cls, code: int = 200, msg: str = "success", data: T = None) -> Self:
        return cls(code=code, msg=msg, data=data)

    @classmethod
    def failure(cls, code: int = 400, msg: str = "failure", data: T = None) -> Self:
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

write_base_tortoise_model_py_code="""
from tortoise import Model
from tortoise import fields

class AbstractModel(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


    def __str__(self) -> str:
        attributes = ', '.join(f"{key}={value}" for key, value in self.__dict__.items() if not key.startswith('_'))
        return f"{self.__class__.__name__}({attributes})"

    
    class Meta: # type: ignore[override]
        abstract = True
"""

write_gitignore_code="""
.venv
.env
.env.*
fastapi-app-manage.toml
"""

def write_gitignore(package:str)->str:
    if package=="poetry":
        return write_gitignore_code+"poetry.lock"
    return write_gitignore_code


def write_base_tortoise_model_py()->str:
    return write_base_tortoise_model_py_code


def write_html()->str:
    return index_html


def write_router(name: str, is_utils: bool = False)->str:
    if is_utils:
        return py_api_router_cbv_code.format(name.title())
    else:
        return py_api_router_code


def write_service(name: str)->str:
    return py_service_code.format(name.title())


def write_schema()->str:
    return py_schema_code


def write_lifespan(db_framwork: str = "tortoise-orm")->str:
    if db_framwork == "tortoise-orm":
        return py_lifespan_code.replace(
            "#1", """async with RegisterTortoise(
        app=app,
        config=settings.tortoise_config
    ): """

        )
    else:
        return py_lifespan_code.replace(
            "#1", ""
        )


def write_model(db_framwork: str)->str:
    if db_framwork == "tortoise-orm":
        return py_tortoise_orm_code
    else:
        return py_sqlmodel_code


def write_database()->str:
    return py_core_db


def write_main(cors: bool = False, standard_: bool = False)->str:
    if cors and standard_:
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
        ).replace("#3", "default_response_class=ORJSONResponse").replace("#4",
                                                                         "from fastapi.responses import ORJSONResponse")
    elif cors:
        return py_cors_fastapi_code.replace(
            "#1", """app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
           """).replace("#2", "from fastapi.middleware.cors import CORSMiddleware").replace("#3", "").replace("#4", "")
    elif standard_:
        return py_cors_fastapi_code.replace("#3", "default_response_class=ORJSONResponse").replace("#1", "").replace(
            "#2", "").replace("#4", "from fastapi.responses import ORJSONResponse")
    else:
        return py_cors_fastapi_code.replace("#1", "").replace("#2", "").replace("#3", "").replace("#4", "")


def write_settings(utils: bool = False, db_framework: str = "None"
                   )->str:
    code = py_pydantic_settings_code
    if utils:
        code = py_pydantic_settings_code_

    if db_framework.title() == "None":
        return code.replace("#1", "").replace("#2", "")

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


def write_router_init(name: str)->str:
    return py_router_init_code.format(name=name)

def write_router_init_(name: str)->str:
    app_path = pathlib.Path("app")
    router_path = app_path / "router"
    router_path_init = router_path / "__init__.py"
    try:
        code = router_path_init.read_text()
        index = code.find("from fastapi import APIRouter")
        if index != -1:
            update_index = index + len("from fastapi import APIRouter")
            update_code = code[:update_index] + f"\nfrom .{name} import router as {name}_router" + code[update_index:]
            return update_code
        typer.echo("Cannot rewrite router __init__.py", err=True)
        return code
    except UnicodeDecodeError:
        typer.echo("Error reading __init__.py. The file may contain non-UTF-8 characters.", err=True)
        return ""


def write_result()->str:
    return py_standard_response_code
