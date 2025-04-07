from InventoryService.app.db.connections import AsyncPostgresSQLDB

db = AsyncPostgresSQLDB()


async def startup():
    await db.initialize({
        "user": "workspace",
        "password": "",
        "database": "test_db",
        "host": "localhost",
        "port": 5432
    })


async def shutdown():
    await db.close()
