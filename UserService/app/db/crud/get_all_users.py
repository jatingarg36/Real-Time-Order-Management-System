from typing import List

from fastapi_pagination import Params

from UserService.app.db.connections import AsyncPostgresSQLDB
from UserService.app.db.models.users import User
from UserService.configuration import config

db = AsyncPostgresSQLDB()


async def action(params: Params) -> List[User]:
    async with db._pool.acquire() as connection:
        async with connection.transaction():
            user_list = await connection.fetch(
                f"SELECT * FROM {config.USER_TABLE_NAME} "
                f"ORDER BY created_at DESC "
                f"LIMIT $1 OFFSET $2    ",
                params.size, (params.page - 1) * params.size
            )
            print(user_list)
            return [User(**dict(user)) for user in user_list]
