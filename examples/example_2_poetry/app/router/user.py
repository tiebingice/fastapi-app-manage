
from fastapi_utils.cbv import cbv
from fastapi import APIRouter
router = APIRouter()

@cbv(router)
class UserView:

    @router.get("/")
    async def get(self):
        return
