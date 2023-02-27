from fastapi import APIRouter

from adapters.presenter.api_response import APIResponse
from drivers.db.mysql import Mysql
from usecase.hoge.get_hoges import GetHoges

# FastAPIのルーター
router = APIRouter()


@router.get('/api/hoge')
async def get_hoges() -> dict:
    """ ほげ一覧を取得するAPI """
    return GetHoges(APIResponse(), Mysql()).get_hoges()
