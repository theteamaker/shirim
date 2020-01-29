import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
USERS_DB = os.getenv("USERS_DB")