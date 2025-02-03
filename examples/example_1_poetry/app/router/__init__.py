
from fastapi import APIRouter
from .tail import router as tail_router
from .user import router as user_router
router = APIRouter()
