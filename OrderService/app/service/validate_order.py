from typing import List

from OrderService.app.db.models.order import OrderItems
from OrderService.configuration import config


async def action(order_items: List[OrderItems], inventory_cache):
    for item in order_items:
        if not inventory_cache.hexists(config.INVENTORY_REDIS_KEY, str(item.item_id)):
            return False
    return True
