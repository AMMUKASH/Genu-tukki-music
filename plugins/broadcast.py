from pyrogram import Client, filters
from utils.logger import send_log

OWNER_ID = 123456789  # Replace with your numeric Telegram ID

@Client.on_message(filters.command("broadcastall") & filters.user(OWNER_ID))
async def broadcast_all(client, message):
    await message.reply_text("Broadcast sent to all users + groups + assistants.")
    await send_log(client, f"BroadcastAll triggered by {message.from_user.id}")

@Client.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(client, message):
    await message.reply_text("Broadcast sent to users + groups.")
    await send_log(client, f"Broadcast triggered by {message.from_user.id}")
