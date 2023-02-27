from fastapi import APIRouter

from adapters.presenter.api_response import APIResponse
from drivers.db.mysql import Mysql
from entities.dto.user.input_insert_user_dto import InputInsertUserDto

from entities.dto.user.input_update_user_dto import InputUpdateUserDto
from usecase.users.delete_selected_user import DeleteSelectedUser
from usecase.users.get_selected_user import GetSelectedUser
from usecase.users.get_users import GetUsers
from usecase.users.insert_user import InsertSelectedUser
from usecase.users.update_selected_user import UpdateSelectedUser

# FastAPIのルーター
router = APIRouter()


@router.get('/api/users')
async def get_users() -> dict:
    """ 全ユーザー情報を取得するAPI """
    return GetUsers(APIResponse(), Mysql()).get()


@router.get('/api/users/{user_id}')
async def get_selected_user(user_id: str) -> dict:
    """ 特定のユーザー情報を取得するAPI """
    return GetSelectedUser(APIResponse(), Mysql()).get(user_id)


@router.post('/api/users/{user_id}')
async def update_selected_user(user_id: str, request_body: InputUpdateUserDto) -> dict:
    """ 特定のユーザー情報を更新するAPI """
    return UpdateSelectedUser(APIResponse(), Mysql()).update(user_id, request_body.dict())


@router.put('/api/users/')
async def insert_selected_user(request_body: InputInsertUserDto) -> dict:
    """ ユーザーを追加するAPI """
    return InsertSelectedUser(APIResponse(), Mysql()).insert(request_body.dict())


@router.delete('/api/users/{user_id}')
async def delete_selected_user(user_id: str) -> dict:
    """ 特定のユーザーを削除するAPI """
    return DeleteSelectedUser(APIResponse(), Mysql()).delete(user_id)
