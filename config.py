import os 
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TG_API_KEY")
DB_NAME = "pet_bot.db"

TIME_INTERVAL = 10 # интервал уменьшения показателей в сек

DECREASE_PARAMS = {
    "hunger": -5,
    "energy": -3,
    "happiness": -1,
    "friendliness": -2,
}