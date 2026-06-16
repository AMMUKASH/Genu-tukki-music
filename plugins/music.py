from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls.types.input_stream import InputStream, AudioPiped
import yt_dlp
import asyncio
from utils.logger import send_log
import config

# Initialize Pyrogram with STRING_SESSION
app = Client(
    config.BOT_USERNAME,
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    session_string="AQJF8NUAgBfq_JynQDTlV8Bw7YUi_5Xr8Y_0JWiGElK7XrAUyeBr9Iu87Heq8j3EZ42zuFbbJgv1RmgkNt0CErphSozbaL0sG8TYIm9RqPPYTRR3LmeNGkGkb"
)

pytgcalls = PyTgCalls(app)

# Queue system: {chat_id: [list of songs]}
queues = {}

# Helper: download audio from YouTube
async def download_audio(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "quiet": True,
    }
    loop = asyncio.get_event_loop()
    def run_ydl():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)
    return await loop.run_in_executor(None, run_ydl)

# Play next track in queue
async def play_next(chat_id):
    if queues.get(chat_id):
        file_path = queues[chat_id].pop(0)
        await pytgcalls.join_group_call(
            chat_id,
            InputStream(AudioPiped(file_path))
        )
        await send_log(app, f"▶️ Next track started in chat {chat_id}")
    else:
        await pytgcalls.leave_group_call(chat_id)
        await send_log(app, f"⏹ Queue empty, left VC in chat {chat_id}")

# Command: /play
@app.on_message(filters.command("play") & filters.group)
async def play_music(client, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Please provide a song name or link.")
    
    query = message.text.split(None, 1)[1]
    await message.reply_text(f"🔎 Searching: {query}")
    
    file_path = await download_audio(query)
    chat_id = message.chat.id
    
    if chat_id not in queues:
        queues[chat_id] = []
    
    if not queues[chat_id]:
        queues[chat_id].append(file_path)
        await pytgcalls.join_group_call(
            chat_id,
            InputStream(AudioPiped(file_path))
        )
        await message.reply_text("🎶 Now playing your track!")
        await send_log(client, f"🎶 Play started in {message.chat.title}")
    else:
        queues[chat_id].append(file_path)
        await message.reply_text("➕ Added to queue!")
        await send_log(client, f"➕ Track queued in {message.chat.title}")

# Command: /skip
@app.on_message(filters.command("skip") & filters.group)
async def skip_music(client, message):
    chat_id = message.chat.id
    if queues.get(chat_id):
        await pytgcalls.leave_group_call(chat_id)
        await play_next(chat_id)
        await message.reply_text("⏭ Skipped to next track!")
        await send_log(client, f"⏭ Skip used in {message.chat.title}")
    else:
        await message.reply_text("❌ Queue is empty.")

# Command: /queue
@app.on_message(filters.command("queue") & filters.group)
async def show_queue(client, message):
    chat_id = message.chat.id
    if queues.get(chat_id):
        text = "🎶 **Current Queue:**\n"
        for i, song in enumerate(queues[chat_id], start=1):
            text += f"{i}. {song}\n"
        await message.reply_text(text)
    else:
        await message.reply_text("❌ Queue is empty.")

# Command: /stop
@app.on_message(filters.command("stop") & filters.group)
async def stop_music(client, message):
    chat_id = message.chat.id
    queues[chat_id] = []
    await pytgcalls.leave_group_call(chat_id)
    await message.reply_text("⏹ Music stopped and queue cleared.")
    await send_log(client, f"⏹ Stop used in {message.chat.title}")

# Command: /pause
@app.on_message(filters.command("pause") & filters.group)
async def pause_music(client, message):
    chat_id = message.chat.id
    await pytgcalls.pause_stream(chat_id)
    await message.reply_text("⏸ Music paused.")
    await send_log(client, f"⏸ Pause used in {message.chat.title}")

# Command: /resume
@app.on_message(filters.command("resume") & filters.group)
async def resume_music(client, message):
    chat_id = message.chat.id
    await pytgcalls.resume_stream(chat_id)
    await message.reply_text("▶️ Music resumed.")
    await send_log(client, f"▶️ Resume used in {message.chat.title}")

# Auto play next when track ends
@pytgcalls.on_stream_end()
async def on_stream_end(_, update):
    chat_id = update.chat_id
    await play_next(chat_id)

async def main():
    await app.start()
    await pytgcalls.start()
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
