"Configuration file for the app"
import os

DATABASE_URL = os.getenv("DB_URL")
BOOK_FILEPATH = os.getenv("BOOK_FILEPATH")
SOLUTIONS_FILEPATH = os.getenv("SOLUTIONS_FILEPATH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
