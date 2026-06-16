from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient
from utils.logger import send_log
import config

OWNER_ID = 123456789  # Replace with your numeric Telegram ID

# MongoDB connection
mongo_client = AsyncIOMotorClient(config.MONGO_URL)
db = mongo_client["tukki_music_db"]
users = db["users"]
groups = db["groups"]

# Auto-save users/groups when they interact
@Client.on_message(filters.private)
async def save_user(client, message):
    await users.update_one({"user_id": message.from_user.id}, {"$set": {"user_id": message.from_user.id}}, upsert=True)

@Client.on_message(filters.group)
async def save_group(client, message):
    await groups.update_one({"chat_id": message.chat.id}, {"$set": {"chat_id": message.chat.id}}, upsert=True)

# Command: /broadcast → send to users + groups
@Client.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(client, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Provide a message to broadcast.")
    text = message.text.split(None, 1)[1]

    # Send to users
    async for user in users.find({}):
        try:
            await client.send_message(user["user_id"], text)
        except:
            pass

    # Send to groups
    async for group in groups.find({}):
        try:
            await client.send_message(group["chat_id"], text)
        except:
            pass

    await message.reply_text("📢 Broadcast sent to users + groups.")
    await send_log(client, f"📢 Broadcast triggered by {message.from_user.mention}")

# Command: /broadcastall → send to users + groups + assistants
@Client.on_message(filters.command("broadcastall") & filters.user(OWNER_ID))
async def broadcast_all(client, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Provide a message to broadcast.")
    text = message.text.split(None, 1)[1]

    # Send to users
    async for user in users.find({}):
        try:
            await client.send_message(user["user_id"], text)
        except:
            pass

    # Send to groups
    async for group in groups.find({}):
        try:
            await client.send_message(group["chat_id"], text)
        except:
            pass

    # Assistants (optional: add another DB collection if needed)
    await message.reply_text("📢 Broadcast sent to all (users + groups + assistants).")
    await send_log(client, f"📢 BroadcastAll triggered by {message.from_user.mention}")
