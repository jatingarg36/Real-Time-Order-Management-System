from InventoryService.app.db.connections import AsyncPostgresSQLDB
from InventoryService.app.db.models.inventory import Item
from InventoryService.configuration import config

db = AsyncPostgresSQLDB()


async def action(create_item: Item):
    result = await db.execute(
        f"INSERT INTO {config.INVENTORY_TABLE_NAME} "
        f"(store_id, item_id, item_name, item_description, price, quantity, alert_threshold, updated_at) "
        f"VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING item_id",
        create_item.store_id, create_item.item_id, create_item.item_name, create_item.item_description,
        create_item.price, create_item.quantity, create_item.alert_threshold, create_item.updated_at
    )
    return result
