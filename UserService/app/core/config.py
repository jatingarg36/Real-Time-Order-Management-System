from UserService.app.db.connections import AsyncPostgresSQLDB
from UserService.configuration import config

db = AsyncPostgresSQLDB()


async def startup():
    await db.initialize({
        "user": config.DB_USER,
        "password": config.DB_PASSWORD,
        "database": config.DB_NAME,
        "host": config.DB_HOST,
        "port": config.DB_PORT
    })


async def shutdown():
    await db.close()
