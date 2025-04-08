from datetime import datetime

from InventoryService.app.db.connections import AsyncPostgresSQLDB
from InventoryService.app.schemas.inventory_schema import ItemUpdate
from InventoryService.configuration import config

db = AsyncPostgresSQLDB()


async def action(updates: ItemUpdate):
    async with db._pool.acquire() as conn:
        async with conn.transaction():
            query = f"""
                UPDATE {config.INVENTORY_TABLE_NAME}
                SET
                    quantity = quantity + $1,
                    price = COALESCE($2, price),
                    alert_threshold = COALESCE($3, alert_threshold),
                    updated_at = $4
                WHERE
                    store_id = $5 AND item_id = $6
            """
            await conn.execute(
                query,
                updates.add_quantity,
                updates.new_price,
                updates.new_alert_threshold,
                datetime.now(),
                updates.store_id,
                updates.item_id
            )
