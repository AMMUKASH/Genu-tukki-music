import os
import logging
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import InputStream, AudioPiped

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
    # Example: play audio from yt-dlp
    await call.join_group_call(
        message.chat.id,
        InputStream(
            AudioPiped(song)  # yt-dlp link or file path
        )
    )

@app.on_message(filters.command("stop"))
async def stop(_, message):
    await call.leave_group_call(message.chat.id)
    await message.reply_text("⏹️ Stopped playback.")

if __name__ == "__main__":
    LOGGER.info("Starting Tukki Music Bot...")
    app.start()
    call.start()
    LOGGER.info("Bot is running...")
    app.idle()
