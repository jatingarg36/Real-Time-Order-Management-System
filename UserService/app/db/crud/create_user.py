from UserService.app.db.connections import AsyncPostgresSQLDB
from UserService.app.db.models.users import User
from UserService.configuration import config

db = AsyncPostgresSQLDB()


async def action(new_user: User):
    try:
        async with db._pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.execute(
                    f"INSERT INTO {config.USER_TABLE_NAME} "
                    "(user_id,username, created_at) "
                    f"VALUES ($1, $2, $3)",
                    new_user.user_id, new_user.username, new_user.created_at
                )
                if result:
                    return True
    except Exception as e:
        print("Error occurred:", e)
