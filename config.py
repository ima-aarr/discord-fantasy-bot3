import os
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN') or os.getenv('DISCORD_TOKEN')
FIREBASE_URL = os.getenv('FIREBASE_URL')
FIREBASE_SECRET = os.getenv('FIREBASE_SECRET')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPSEEK_MODEL = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')
DEEPSEEK_BASE = os.getenv('DEEPSEEK_BASE', 'https://api.deepseek.com/v1')
LLM_PROXY_URL = os.getenv('LLM_PROXY_URL')
ADMIN_USER_IDS = [x.strip() for x in os.getenv('ADMIN_USER_IDS','').split(',') if x.strip()]
# BOT_OWNER_ID can be set via environment variable BOT_OWNER_ID; fallback to provided ID only if env not set.
BOT_OWNER_ID = os.getenv('BOT_OWNER_ID', '1382985288841826354')
RATE_LIMIT_USER = int(os.getenv('RATE_LIMIT_USER','10'))
RATE_LIMIT_GLOBAL = int(os.getenv('RATE_LIMIT_GLOBAL','200'))
PORT = int(os.getenv('PORT','8000'))
