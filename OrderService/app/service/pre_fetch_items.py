import json

import httpx

from OrderService.configuration import config


async def pre_fetch_items(app):
    redis_client = app.state.redis_client
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{config.INVENTORY_SERVICE_URL}/api/v1/inventory/all_items")
            if response.status_code == 200:
                all_items = response.json()
                for item in all_items:
                    item_id = item.get('item_id')
                    if item:
                        redis_client.hset(config.INVENTORY_REDIS_KEY, str(item_id), json.dumps(item))
    except Exception as e:
        print(f"Error while pre fetching data for inventory cache : {e}")
