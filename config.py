import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Database
DB_NAME = "leads.db"

# API
SCRAPER_API = os.getenv("SCRAPER_API")  # Optional
