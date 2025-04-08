from collections import defaultdict
from typing import List

from fastapi_pagination import Params

from OrderService.app.db.connections import AsyncPostgresSQLDB
from OrderService.app.schemas.order_schema import OrderResponse
from OrderService.configuration import config

db = AsyncPostgresSQLDB()


async def action(user_id: str, params: Params, encoder) -> List[OrderResponse]:
    async with db._pool.acquire() as connection:
        async with connection.transaction():
            orders = await connection.fetch(
                f"WITH limited_orders AS "
                f"(SELECT * FROM {config.ORDER_TABLE_NAME} "
                f"WHERE user_id = $1 ORDER BY created_at DESC "
                f"LIMIT $2 OFFSET $3) "
                f"SELECT o.*, i.item_id, i.quantity "
                f"FROM limited_orders o "
                f"JOIN {config.ORDER_ITEM_TABLE_NAME} i "
                f"ON o.order_id = i.order_id",
                user_id, params.size, (params.page - 1) * params.size
            )
            grouped = defaultdict(list)
            for record in orders:
                grouped[record['order_id']].append(record)

            return [encoder(group) for group in grouped.values()]
