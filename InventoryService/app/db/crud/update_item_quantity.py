from InventoryService.app.db.connections import AsyncPostgresSQLDB
from InventoryService.configuration import config

db = AsyncPostgresSQLDB()


async def action(order_items):
    low_quantity_items = []
    insufficient_items = []
    item_details = {}

    async with db._pool.acquire() as conn:
        async with conn.transaction():

            for item in order_items:
                item_id = item["item_id"]
                requested_quantity = item["quantity"]

                if requested_quantity <= 0:
                    raise ValueError(f"Quantity for item {item_id} must be positive.")

                row = await conn.fetchrow(
                    f"""
                    SELECT quantity, alert_threshold
                    FROM {config.INVENTORY_TABLE_NAME}
                    WHERE item_id = $1
                    FOR UPDATE; 
                    """,
                    item_id
                )

                if not row:
                    raise ValueError(f"Item {item_id} does not exist.")

                current_stock = row["quantity"]
                alert_threshold = row["alert_threshold"]

                if current_stock < requested_quantity:
                    insufficient_items.append(item_id)
                elif (current_stock - requested_quantity) <= alert_threshold:
                    low_quantity_items.append(item_id)

                item_details[item_id] = {
                    "requested_quantity": requested_quantity  # Needed for the update query
                }
            if len(insufficient_items) > 0:
                raise Exception(
                    f"Insufficient stock for items: {insufficient_items}. "
                )
            for item_id, details in item_details.items():
                await conn.execute(
                    f"""
                    UPDATE {config.INVENTORY_TABLE_NAME}
                    SET quantity = quantity - $1 
                    WHERE item_id = $2;
                    """,
                    details["requested_quantity"],
                    item_id
                )
    return low_quantity_items
