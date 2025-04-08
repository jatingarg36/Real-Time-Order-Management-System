from typing import List

from OrderService.app.db.connections import AsyncPostgresSQLDB
from OrderService.app.db.models.order import Order, OrderItems
from OrderService.configuration import config

db = AsyncPostgresSQLDB()


async def action(order: Order, order_items: List[OrderItems]):
    try:
        async with db._pool.acquire() as connection:
            async with connection.transaction():
                # 1. Insert into orders and get order_id
                await connection.execute(
                    f"INSERT INTO {config.ORDER_TABLE_NAME} "
                    "(order_id,status,user_id,store_id,total_amount,payment_id,created_at,updated_at) "
                    f"VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING order_id",
                    order.order_id, order.status, order.user_id, order.store_id, order.total_amount,
                    order.payment_id, order.created_at, order.updated_at
                )
                print(f"Inserted order_id: {order.order_id}")

                # 2. Insert items associated with the order
                insert_items_query = f"""
                        INSERT INTO {config.ORDER_ITEM_TABLE_NAME} (order_id, item_id, quantity)
                        VALUES ($1, $2, $3);
                    """
                # Use a batch of executemany
                await connection.executemany(
                    insert_items_query,
                    [(item.order_id, item.item_id, item.quantity) for item in order_items]
                )
                print("Order items inserted.")

    except Exception as e:
        print("Error occurred:", e)
