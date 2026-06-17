import os
import logging
import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped

# Config from environment
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
STRING_SESSION = os.getenv("STRING_SESSION")
LOG_GROUP = int(os.getenv("LOG_GROUP"))

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
    
    await call.join_group_call(
        message.chat.id,
        AudioPiped(song)
    )

@app.on_message(filters.command("stop"))
async def stop(_, message):
    await call.leave_group_call(message.chat.id)
    await message.reply_text("⏹️ Stopped playback.")

# Python 3.14+ loop issue fix karne ke liye main async function
async def main():
    LOGGER.info("Starting Tukki Music Bot...")
    await app.start()
    await call.start()
    LOGGER.info("Bot is running...")
    await asyncio.Event().wait()  # Bot ko running state me rakhne ke liye

if __name__ == "__main__":
    # Naye Python versions ke liye event loop manually initialize karna
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        LOGGER.info("Bot stopped.")
