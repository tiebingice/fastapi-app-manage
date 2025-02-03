
from fastapi_utils.cbv import cbv
from fastapi import APIRouter
router = APIRouter()

@cbv(router)
class TailView:

    @router.get("/")
    async def get(self):
        return
