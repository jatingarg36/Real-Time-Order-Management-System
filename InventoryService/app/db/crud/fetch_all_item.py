from typing import List, Optional

from InventoryService.app.db.connections import AsyncPostgresSQLDB
from InventoryService.app.db.models.inventory import Item
from InventoryService.configuration import config

db = AsyncPostgresSQLDB()


async def action(store_id: Optional[str]) -> List[Item]:
    async with db._pool.acquire() as conn:
        async with conn.transaction():
            if store_id:
                rows = await conn.fetch(f"SELECT * from {config.INVENTORY_TABLE_NAME} WHERE store_id = $1", store_id)
            else:
                rows = await conn.fetch(f"SELECT * from {config.INVENTORY_TABLE_NAME}")
            return [Item(**dict(row)) for row in rows]
