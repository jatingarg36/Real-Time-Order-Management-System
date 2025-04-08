from InventoryService.app.db.connections import AsyncPostgresSQLDB
from InventoryService.app.db.models.inventory import Item
from InventoryService.configuration import config

db = AsyncPostgresSQLDB()


async def action(item_id: str) -> Item:
    async with db._pool.acquire() as conn:
        async with conn.transaction():
            return await conn.fetchrow(f"SELECT * from {config.INVENTORY_TABLE_NAME} WHERE item_id = $1", item_id)
