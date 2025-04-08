import socket

from aiokafka import AIOKafkaProducer

from OrderService.configuration import config

_kafka_producer = None


async def get_kafka_producer():
    global _kafka_producer
    if _kafka_producer is None:
        _kafka_producer = AIOKafkaProducer(bootstrap_servers=config.KAFKA_SERVER,
                                           client_id=socket.gethostname(),
                                           linger_ms=10, max_batch_size=500)
        await _kafka_producer.start()
    return _kafka_producer
