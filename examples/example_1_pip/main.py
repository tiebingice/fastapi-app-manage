
from fastapi import FastAPI
from app.core.lifespan import lifespan
from app.router import router


app = FastAPI(
    lifespan=lifespan
)


