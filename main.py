import os
import logging
import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream  # v3 dev24 ke liye direct import

# Config from environment (safe fallback)
API_ID = os.getenv("API_ID")
if not API_ID:
    raise ValueError("API_ID environment variable not set!")
API_ID = int(API_ID)

API_HASH = os.getenv("API_HASH") or ""
BOT_TOKEN = os.getenv("BOT_TOKEN") or ""
STRING_SESSION = os.getenv("STRING_SESSION") or ""
LOG_GROUP = int(os.getenv("LOG_GROUP") or 0)

# Logging setup
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# Pyrogram client
app = Client(
    "TukkiMusicBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    session_string=STRING_SESSION
)

# PyTgCalls client
call = PyTgCalls(app)

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("🎶 Tukki Music Bot is alive!")

@app.on_message(filters.command("play"))
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Please provide a song name or link.")
    
    song = message.text.split(None, 1)[1]
    await message.reply_text(f"▶️ Playing: {song}")
    
    # Latest pytgcalls syntax: MediaStream use karke path/link pass karna
    await call.join_group_call(
        message.chat.id,
        MediaStream(song)
    )

@app.on_message(filters.command("stop"))
async def stop(_, message):
    await call.leave_group_call(message.chat.id)
    await message.reply_text("⏹️ Stopped playback.")

if __name__ == "__main__":
    LOGGER.info("Starting Tukki Music Bot...")

    # Asyncio event loop fix for Python 3.14
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Run bot inside event loop
    async def run():
        await app.start()
        await call.start()
        LOGGER.info("Bot is running...")
        await app.idle()

    loop.run_until_complete(run())
