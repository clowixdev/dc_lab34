from os import environ

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from keras import models

from database.dbworker import create_db_engine
# from scripts.predictor import tensorflow_init

# model = tensorflow_init()
# model.save("./scripts/model.keras")
model = models.load_model("./scripts/model.keras")

load_dotenv(".env")

bot = Bot(
    token=environ.get("TOKEN"),
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

engine = create_db_engine()
dp = Dispatcher(storage=MemoryStorage())

ADMIN_ID = 625438726
BOT_TOKEN = environ.get("TOKEN")
HOST = environ.get("HOST")
PORT = int(environ.get("PORT"))
WEBHOOK_PATH = f"/{BOT_TOKEN}"
TUNA = environ.get("TUNA")