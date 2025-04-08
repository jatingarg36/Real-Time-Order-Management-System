from OrderService.app.db.connections import AsyncPostgresSQLDB
from OrderService.app.schemas.order_schema import OrderResponse
from OrderService.configuration import config

db = AsyncPostgresSQLDB()


async def action(order_id: str, user_id: str, encoder) -> OrderResponse | None:
    try:
        async with db._pool.acquire() as connection:
            async with connection.transaction():
                order = await connection.fetch(
                    f"""SELECT * 
                        FROM {config.ORDER_TABLE_NAME} o 
                        JOIN {config.ORDER_ITEM_TABLE_NAME} i ON o.order_id = i.order_id 
                        WHERE o.order_id = $1 AND o.user_id = $2
                        """,
                    order_id, user_id
                )
                return encoder(order)
    except Exception as e:
        print("Error occurred:", e)
        return None
