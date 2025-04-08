from OrderService.app.db.connections import AsyncPostgresSQLDB
from OrderService.configuration import config

db = AsyncPostgresSQLDB()


async def action(order_id: str):
    try:
        async with db._pool.acquire() as connection:
            async with connection.transaction():
                # 1. Insert into orders and get order_id
                order = await connection.fetchrow(
                    "SELECT status "
                    f"FROM {config.ORDER_TABLE_NAME} "
                    "WHERE order_id = $1",
                    order_id
                )
                print(f"Status of order_id: {order_id} is {order['status']}")
    except Exception as e:
        print("Error occurred:", e)
