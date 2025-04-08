import os
import pathlib

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv(verbose=True, override=True)

BRANCH = os.environ.get('branch')
if BRANCH == "develop":
    base_dir = pathlib.Path(__file__).parent
    load_dotenv(base_dir, override=True)
    response_secrets = {k: v for k, v in os.environ.items()}


class GlobalConfig(BaseSettings):
    DB_NAME: str = response_secrets["DB_NAME"]
    DB_HOST: str = response_secrets["DB_HOST"]
    DB_PORT: str = response_secrets["DB_PORT"]
    DB_USER: str = response_secrets["DB_USER"]
    DB_PASSWORD: str = response_secrets["DB_PASSWORD"]

    ORDER_TABLE_NAME: str = response_secrets["ORDER_TABLE_NAME"]
    ORDER_ITEM_TABLE_NAME: str = response_secrets["ORDER_ITEM_TABLE_NAME"]
    INVENTORY_REDIS_KEY: str = response_secrets["INVENTORY_REDIS_KEY"]

    KAFKA_SERVER: str = response_secrets["KAFKA_SERVER"]
    ORDER_PLACE_KAFKA_TOPIC: str = response_secrets["ORDER_PLACE_KAFKA_TOPIC"]
    ORDER_STATUS_UPDATE_KAFKA_TOPIC: str = response_secrets["ORDER_STATUS_UPDATE_KAFKA_TOPIC"]
    NEW_ITEM_ALERT_KAFKA_TOPIC: str = response_secrets["NEW_ITEM_ALERT_KAFKA_TOPIC"]
    ORDER_CANCEL_KAFKA_TOPIC: str = response_secrets["ORDER_CANCEL_KAFKA_TOPIC"]

    REDIS_HOST: str = response_secrets["REDIS_HOST"]
    REDIS_PORT: str = response_secrets["REDIS_PORT"]

    INVENTORY_SERVICE_URL: str = response_secrets["INVENTORY_SERVICE_URL"]



config = GlobalConfig()
