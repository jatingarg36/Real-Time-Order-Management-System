from OrderService.app.db.connections import AsyncPostgresSQLDB
from OrderService.app.db.models.order import OrderUpdate
from OrderService.configuration import config

db = AsyncPostgresSQLDB()


async def action(order_updates: OrderUpdate):
    try:
        async with db._pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    f"""
                       UPDATE {config.ORDER_TABLE_NAME}
                       SET status = $1, updated_at = $2
                       WHERE order_id = $3;
                       """,
                    order_updates.status, order_updates.updated_at, order_updates.order_id
                )
    except Exception as e:
        print("Error occurred:", e)
