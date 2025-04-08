import uuid
from datetime import datetime

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi_pagination import Params

from UserService.app.db.crud import get_all_users, create_user
from UserService.app.db.models.users import User
from UserService.app.schemas.user_create import NewUser

router = APIRouter(prefix='/user')


@router.get('/all', description='Fetch all the users')
async def action(params: Params = Depends()):
    return await get_all_users.action(params)


@router.post('', description="Api endpoint to create a new user")
async def action(new_user: NewUser):
    user = User(user_id=uuid.uuid4(), username=new_user.username, created_at=datetime.now())
    print(user)
    iscreated = await create_user.action(user)
    if iscreated:
        return user
    raise Exception("Unable to create new user")