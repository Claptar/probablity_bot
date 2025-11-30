"Configuration file for the app"

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DB_URL")
BOOK_FILEPATH = os.getenv("BOOK_FILEPATH")
SOLUTION_MANNUAL_FILE = os.getenv("SOLUTION_MANNUAL_FILE")
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SECTION_LIST = os.getenv("SECTION_LIST")
SUBSECTION_FILES_DIR = os.getenv("SUBSECTION_FILES_DIR")
ELEMENT_TYPES_LIST = os.getenv("ELEMENT_TYPES_LIST")
