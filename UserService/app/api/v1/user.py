import uuid
from datetime import datetime
from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi_pagination import Params

from UserService.app.db.crud import get_all_users, create_user
from UserService.app.db.models.users import User
from UserService.app.schemas.user_create import NewUser

router = APIRouter(prefix='/user')


@router.get('/all', response_model=List[User],
            description="Retrieve a paginated list of all registered users.")
async def action(params: Params = Depends()):
    return await get_all_users.action(params)


@router.post('', response_model=User,
             description="Create a new user with a unique username and registration timestamp.")
async def action(new_user: NewUser):
    user = User(user_id=uuid.uuid4(), username=new_user.username, created_at=datetime.now())
    if await create_user.action(user):
        return user
    raise Exception("Unable to create new user")
