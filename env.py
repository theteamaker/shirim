import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("SHIRIM_TOKEN")
LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
USERS_DB = os.getenv("SHIRIM_USERS_DB")
SERVERS_DB = os.getenv("SHIRIM_SERVERS_DB")
