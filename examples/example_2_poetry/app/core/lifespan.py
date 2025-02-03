
from contextlib import asynccontextmanager
from fastapi import FastAPI
from tortoise.contrib.fastapi import RegisterTortoise
from settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    #1
        yield

