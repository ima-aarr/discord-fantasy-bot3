import threading, logging, os, asyncio
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import discord
from discord.ext import commands
from config import DISCORD_BOT_TOKEN, PORT
if not DISCORD_BOT_TOKEN:
    raise RuntimeError('DISCORD_BOT_TOKEN not set')
def start_health():
    handler=SimpleHTTPRequestHandler
    with TCPServer(('', PORT), handler) as httpd:
        print(f'Health server on {PORT}'); httpd.serve_forever()
threading.Thread(target=start_health, daemon=True).start()
intents = discord.Intents.default(); intents.message_content=True; intents.members=True; intents.guilds=True
bot = commands.Bot(command_prefix='/', intents=intents)
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} ({bot.user.id})')
    try:
        await bot.load_extension('cogs.admin_cog'); print('Loaded admin_cog')
    except Exception as e: print('Fail load admin_cog', e)
    try: await bot.tree.sync(); print('Slash commands synced')
    except Exception as e: print('Sync failed', e)
if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(bot.start(DISCORD_BOT_TOKEN))
