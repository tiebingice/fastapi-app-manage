
from fastapi import FastAPI
from app.core.lifespan import lifespan
from app.router import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
           
