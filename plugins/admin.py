from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient
from utils.logger import send_log
import config

OWNER_ID = 123456789  # Replace with your numeric Telegram ID

# MongoDB connection
mongo_client = AsyncIOMotorClient(config.MONGO_URL)
db = mongo_client["tukki_music_db"]
auth_users = db["authorized_users"]
banned_users = db["banned_users"]

# Command: /auth → authorize a user
@Client.on_message(filters.command("auth") & filters.user(OWNER_ID))
async def auth_user(client, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Provide a user ID to authorize.")
    user_id = int(message.command[1])
    await auth_users.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)
    await message.reply_text(f"✅ User {user_id} authorized.")
    await send_log(client, f"✅ User {user_id} authorized by {message.from_user.mention}")

# Command: /ban → ban a user
@Client.on_message(filters.command("ban") & filters.user(OWNER_ID))
async def ban_user(client, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Provide a user ID to ban.")
    user_id = int(message.command[1])
    await banned_users.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)
    await message.reply_text(f"🚫 User {user_id} banned.")
    await send_log(client, f"🚫 User {user_id} banned by {message.from_user.mention}")

# Command: /unban → unban a user
@Client.on_message(filters.command("unban") & filters.user(OWNER_ID))
async def unban_user(client, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Provide a user ID to unban.")
    user_id = int(message.command[1])
    await banned_users.delete_one({"user_id": user_id})
    await message.reply_text(f"♻️ User {user_id} unbanned.")
    await send_log(client, f"♻️ User {user_id} unbanned by {message.from_user.mention}")

# Command: /admin → show admin menu
@Client.on_message(filters.command("admin") & filters.user(OWNER_ID))
async def admin_menu(client, message):
    text = """
👑 **Admin Menu**

/auth <user_id> → Authorize user (saved in DB)  
/ban <user_id> → Ban user (saved in DB)  
/unban <user_id> → Unban user (removed from DB)  
/broadcast <msg> → Broadcast to users + groups  
/broadcastall <msg> → Broadcast to all (users + groups + assistants)
"""
    await message.reply_text(text)
    await send_log(client, f"👑 Admin menu accessed by {message.from_user.mention}")
