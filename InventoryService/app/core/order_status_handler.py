import json

from InventoryService.app.core.kafka.producer import get_kafka_producer
from InventoryService.app.schemas.order_update_schema import OrderStatusUpdate
from InventoryService.configuration import config


class OrderStatusHandler:
    def __init__(self, order_update: OrderStatusUpdate):
        self.order_updates = order_update

    async def update(self):
        try:
            producer = await get_kafka_producer()
            await producer.send_and_wait(topic=config.ORDER_STATUS_UPDATE_KAFKA_TOPIC,
                                         value=json.dumps({
                                             "order_id": str(self.order_updates.order_id),
                                             "status": self.order_updates.status.value
                                         }).encode('utf-8'))
            return True
        except Exception as e:
            print(e)
        return False
