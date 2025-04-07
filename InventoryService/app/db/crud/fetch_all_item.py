from typing import List

from InventoryService.app.db.connections import AsyncPostgresSQLDB
from InventoryService.app.db.models.inventory import Item
from InventoryService.configuration import config

db = AsyncPostgresSQLDB()


async def action(store_id: str) -> List[Item]:
    return await db.fetch(f"SELECT * from {config.INVENTORY_TABLE_NAME} WHERE store_id = ($1)", store_id)
