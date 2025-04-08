import json
import uuid
from datetime import datetime
from typing import Optional, List

from InventoryService.app.core.kafka.producer import get_kafka_producer
from InventoryService.app.db.crud import update_item, fetch_item, add_item, fetch_all_item
from InventoryService.app.db.models.inventory import Item
from InventoryService.app.schemas.inventory_schema import ItemUpdate, ItemCreate
from InventoryService.configuration import config


class InventoryHandler:

    async def add_new_item(self, new_item: ItemCreate) -> Item:
        item = Item(**new_item.dict(), item_id=uuid.uuid4(), updated_at=datetime.now())
        await add_item.action(item)
        producer = await get_kafka_producer()
        await producer.send_and_wait(topic=config.NEW_ITEM_ALERT_KAFKA_TOPIC,
                                     value=json.dumps(str(item.item_id)).encode('utf-8'))
        return await fetch_item.action(str(item.item_id))

    async def update_item(self, updates: ItemUpdate) -> Item:
        await update_item.action(updates)
        return await fetch_item.action(str(updates.item_id))

    async def fetch_items(self, store_id: Optional[str]) -> List[Item]:
        return await fetch_all_item.action(store_id)
