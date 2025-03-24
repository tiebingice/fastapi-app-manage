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
        env_file=".env",
        extra="allow"
    )
    #2
    #1

"""

py_pydantic_settings_code_ = """
from fastapi_utils.api_settings import APISettings
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(APISettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"
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

write_base_tortoise_model_py_code = """
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
