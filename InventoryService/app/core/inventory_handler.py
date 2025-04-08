import json
import uuid
from datetime import datetime

from InventoryService.app.core.kafka.producer import get_kafka_producer
from InventoryService.app.db.crud import update_item, fetch_item, add_item, fetch_all_item
from InventoryService.app.db.models.inventory import Item
from InventoryService.app.schemas.inventory_schema import ItemUpdate, ItemCreate
from InventoryService.configuration import config


class InventoryHandler:
    def __init__(self):
        pass

    async def add_new_item(self, new_item: ItemCreate):
        item = Item(**new_item.dict(), item_id=uuid.uuid4(), updated_at=datetime.now())
        await add_item.action(item)
        producer = await get_kafka_producer()
        await producer.send_and_wait(topic=config.NEW_ITEM_ALERT_KAFKA_TOPIC,
                                     value=json.dumps(str(item.item_id)).encode('utf-8'))
        return await fetch_item.action(str(item.item_id))

    async def update_item(self, updates: ItemUpdate):
        await update_item.action(updates)
        return await fetch_item.action(str(updates.item_id))

    async def fetch_items(self, store_id: str):
        return await fetch_all_item.action(store_id)
