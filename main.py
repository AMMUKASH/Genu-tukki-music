import os
import asyncio
from flask import Flask
from threading import Thread
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPcmInputFile
from pymongo import MongoClient

# ==========================================
# 🛠️ 1. CONFIGURATION & CORE VARIABLES
# ==========================================
API_ID = 38138069
API_HASH = "2ed313ebcc45cbcf65d1fc736ec71681"
BOT_TOKEN = "8997247669:AAGCgGGp24DWjRd-7FQ60mat_gQwe2Bs-9Y"
MONGO_URL = "mongodb+srv://misssqn_db_user:Nova01@cluster0.6xxsrwq.mongodb.net/?retryWrites=true&w=majority"
LOG_GROUP = -1003947649552
SUPPORT_CHAT = "https://t.me/Genu_Bot_Support/119"
OWNER_USERNAME = "CoderNova"
BOT_USERNAME = "Tukki_Music_Bot"
START_VIDEO_URL = "https://files.catbox.moe/pnaxj0.mp4"

# Render Environment Variable Mapping for Safety
SESSION_STRING = os.environ.get("SESSION", "AQAAAA...") 

# ==========================================
# 💾 2. DATABASE CLIENT INITIALIZATION
# ==========================================
try:
    mongo_client = MongoClient(MONGO_URL)
    db = mongo_client["TukkiMusicDB"]
    users_col = db["users"]
    groups_col = db["groups"]
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    users_col = None
    groups_col = None

# ==========================================
# 🤖 3. TELEGRAM CLIENTS INITIALIZATION
# ==========================================
bot = Client("TukkiMusicBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
assistant = Client("TukkiAssistant", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
call_py = PyTgCalls(assistant)

# ==========================================
# 🌐 4. FLASK SERVER FOR RENDER (24/7 LIVE)
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "ᴛᴜᴋᴋɪ ᴍᴜsɪᴄ ʙᴏᴛ ɪs ᴀᴄᴛɪᴠᴇ ᴀɴᴅ ʀᴜɴɴɪɴɢ 𝟸𝟺/𝟽"

def run_web_server():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def init_keep_alive():
    t = Thread(target=run_web_server)
    t.start()

# ==========================================
# 🎛️ 5. INLINE KEYBOARDS STRUCTS (SMALL CAPS)
# ==========================================
def get_start_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
        ],
        [
            InlineKeyboardButton("👨‍💻 ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER_USERNAME}"),
            InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url=SUPPORT_CHAT)
        ],
        [
            InlineKeyboardButton("🛠️ ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs", callback_data="help_menu"),
            InlineKeyboardButton("📖 ɢᴜɪᴅᴇ", callback_data="guide_menu")
        ]
    ])

def get_help_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🛡️ ᴀᴅᴍɪɴ", callback_data="cmd_admin"),
            InlineKeyboardButton("🔐 ᴀᴜᴛʜ", callback_data="cmd_auth"),
            InlineKeyboardButton("🎛️ ᴄ-ᴘʟᴀʏ", callback_data="cmd_cplay")
        ],
        [
            InlineKeyboardButton("🔄 ʟᴏᴏᴘ", callback_data="cmd_loop"),
            InlineKeyboardButton("▶️ ᴘʟᴀʏ", callback_data="cmd_play"),
            InlineKeyboardButton("🔀 sʜᴜғғʟᴇ", callback_data="cmd_shuffle")
        ],
        [
            InlineKeyboardButton("⏩ sᴇᴇᴋ", callback_data="cmd_seek"),
            InlineKeyboardButton("⚡ sᴘᴇᴇᴅ", callback_data="cmd_speed"),
            InlineKeyboardButton("🔮 ᴇxᴛʀᴀ", callback_data="cmd_extra")
        ],
        [
            InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_start")
        ]
    ])

def get_back_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="help_menu")]])

# ==========================================
# 📬 6. START COMMAND & DATA SYNC (WITH LOGS)
# ==========================================
@bot.on_message(filters.command("start"))
async def start_handler(_, message: Message):
    user_name = message.from_user.first_name
    is_new_user = False
    
    # Save user data if started in private chat
    if users_col is not None and message.chat.type == message.chat.type.PRIVATE:
        if not users_col.find_one({"user_id": message.from_user.id}):
            users_col.insert_one({"user_id": message.from_user.id, "username": message.from_user.username})
            is_new_user = True

    # Save chat data if started in group
    if message.chat.type != message.chat.type.PRIVATE and groups_col is not None:
        if not groups_col.find_one({"chat_id": message.chat.id}):
            groups_col.insert_one({"chat_id": message.chat.id, "title": message.chat.title})

    if is_new_user:
        log_msg = (
            "🚀 **#ɴᴇᴡ_ᴜsᴇʀ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ**\n\n"
            f"👤 **ᴜsᴇʀ:** {message.from_user.mention}\n"
            f"🆔 **ᴜsᴇʀ ɪᴅ:** `{message.from_user.id}`\n"
            f"🔗 **ᴜsᴇʀɴᴀᴍᴇ:** @{message.from_user.username if message.from_user.username else 'ɴᴏ_ᴜsᴇʀɴᴀᴍᴇ'}"
        )
        try:
            await bot.send_message(LOG_GROUP, log_msg)
        except Exception:
            pass

    caption = (
        f"✨ **ʜᴇʏ** {user_name}!\n"
        f"✨ **ɪ ᴀᴍ** **ᴛᴜᴋᴋɪ ᴍᴜsɪᴄ ʙᴏᴛ 💖🕊️**\n\n"
        "🏆 **ʙᴇsᴛ ǫᴜᴀʟɪᴛʏ ғᴇᴀᴛᴜʀᴇs ɪɴsɪᴅᴇ**\n"
        "🛠️ **ᴍᴀᴅᴇ ʙʏ...** [ᴄᴏᴅᴇʀɴᴏᴠᴀ](https://t.me/CoderNova)\n\n"
        "ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴘ.\n"
        "ᴀsᴋ ʏᴏᴜʀ ᴅᴏᴜʙᴛs ᴀᴛ [sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ](" + SUPPORT_CHAT + ")\n\n"
        "ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : `/`"
    )
    
    try:
        await message.reply_video(
            video=START_VIDEO_URL,
            caption=caption,
            reply_markup=get_start_keyboard()
        )
    except Exception:
        await message.reply_text(
            text=caption,
            reply_markup=get_start_keyboard(),
            disable_web_page_preview=False
        )

# ==========================================
# 🎵 7. MUSIC CONTROL CHANNELS (PRIVATE + PUBLIC)
# ==========================================
@bot.on_message(filters.command(["play", "vplay"]))
async def play_audio(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ **ᴜsᴇ:** `/play [sᴏɴɢ ɴᴀᴍᴇ ᴏʀ ʟɪɴᴋ]`")
    
    query = " ".join(message.command[1:])
    await message.reply_text("🎵 **sᴛʀᴇᴀᴍ ɪs sᴛᴀʀᴛɪɴɢ...**")
    
    chat_id = message.chat.id
    chat_title = message.chat.title if message.chat.title else "ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ"
    
    # Save chat data to DB if missing
    if message.chat.type != message.chat.type.PRIVATE and groups_col is not None:
        if not groups_col.find_one({"chat_id": chat_id}):
            groups_col.insert_one({"chat_id": chat_id, "title": chat_title})

    try:
        # PyTgCalls trigger streaming structure
        await call_py.join_group_call(
            chat_id,
            AudioPcmInputFile("input.raw") 
        )
        
        # Real-time logger
        play_log = (
            "🎵 **#ᴘʟᴀʏ_ʀᴇǫᴜᴇsᴛ sᴛʀᴇᴀᴍ**\n\n"
            f"👥 **ᴄʜᴀᴛ/ɢʀᴏᴜᴘ:** {chat_title}\n"
            f"🆔 **ᴄʜᴀᴛ ɪᴅ:** `{chat_id}`\n"
            f"👤 **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ:** {message.from_user.mention}\n"
            f"🔍 **ǫᴜᴇʀʏ:** `{query}`"
        )
        await bot.send_message(LOG_GROUP, play_log)
        
    except Exception as e:
        await message.reply_text(f"❌ **ᴇʀʀᴏʀ:** {e}")

@bot.on_message(filters.command(["pause", "resume", "skip", "stop", "shuffle", "playlist", "queue", "lyrics", "song", "loop", "seek", "speed"]))
async def music_controls_handler(_, message: Message):
    command = message.command[0].lower()
    chat_title = message.chat.title if message.chat.title else "ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ"
    
    # Ye saare control actions ab private aur public dono chats me seamlessly triggers honge
    try:
        if command == "pause":
            await call_py.pause_stream(message.chat.id)
            await message.reply_text("⏸️ **sᴛʀᴇᴀᴍ ᴘᴀᴜsᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.**")
        elif command == "resume":
            await call_py.resume_stream(message.chat.id)
            await message.reply_text("▶️ **sᴛʀᴇᴀᴍ ʀᴇsᴜᴍᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.**")
        elif command == "skip" or command == "stop":
            await call_py.leave_group_call(message.chat.id)
            await message.reply_text("⏹️ **sᴛʀᴇᴀᴍ sᴛᴏᴘᴘᴇᴅ / sᴋɪᴘᴘᴇᴅ.**")
        else:
            await message.reply_text(f"✨ **ᴄᴏᴍᴍᴀɴᴅ** `/{command}` **ᴇxᴇᴄᴜᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.**")
            
        # Logging Actions to Sudo Log Channel
        action_log = f"⚙️ **#ᴄᴏᴍᴍᴀɴᴅ_ʟᴏɢ:** `/{command}` executed in **{chat_title}** (`{message.chat.id}`) by {message.from_user.mention}"
        await bot.send_message(LOG_GROUP, action_log)
        
    except Exception as e:
        await message.reply_text(f"ℹ️ **ᴍᴜsɪᴄ sᴛʀᴇᴀᴍ ɴᴏᴛ ᴀᴄᴛɪᴠᴇ ʀɪɢʜᴛ ɴᴏᴡ:** {e}")

# ==========================================
# 📥 8. BOT METRICS ROUTING (NEW CHATS JOIN/LEFT LOGS)
# ==========================================
@bot.on_message(filters.new_chat_members)
async def bot_added_log(_, message: Message):
    if any(chat_member.id == (await bot.get_me()).id for chat_member in message.new_chat_members):
        if groups_col is not None:
            if not groups_col.find_one({"chat_id": message.chat.id}):
                groups_col.insert_one({"chat_id": message.chat.id, "title": message.chat.title})
        
        add_log = (
            "📥 **#ᴀheader #ᴊᴏɪɴ_ɢʀᴏᴜᴘ**\n\n"
            f"👥 **ɢʀᴏᴜᴘ ɴᴀᴍᴇ:** {message.chat.title}\n"
            f"🆔 **ɢʀᴏᴜᴘ ɪᴅ:** `{message.chat.id}`\n"
            f"👤 **ᴀᴅᴅᴇᴅ ʙʏ:** {message.from_user.mention if message.from_user else 'ᴜɴᴋɴᴏᴡɴ'}"
        )
        try:
            await bot.send_message(LOG_GROUP, add_log)
        except Exception:
            pass

@bot.on_message(filters.left_chat_member)
async def bot_kicked_log(_, message: Message):
    if message.left_chat_member.id == (await bot.get_me()).id:
        if groups_col is not None:
            groups_col.delete_one({"chat_id": message.chat.id})
            
        left_log = (
            "📤 **#ʟᴇғᴛ_ɢʀᴏᴜᴘ #ᴋɪᴄᴋᴇᴅ**\n\n"
            f"👥 **ɢʀᴏᴜᴘ ɴᴀᴍᴇ:** {message.chat.title}\n"
            f"🆔 **ɢʀᴏᴜᴘ ɪᴅ:** `{message.chat.id}`\n"
            f"👤 **ʀᴇᴍᴏᴠᴇᴅ ʙʏ:** {message.from_user.mention if message.from_user else 'ᴜɴᴋɴᴏᴡɴ'}"
        )
        try:
            await bot.send_message(LOG_GROUP, left_log)
        except Exception:
            pass

# ==========================================
# 🎛️ 9. CALLBACK DYNAMIC MENUS INTERFACES
# ==========================================
@bot.on_callback_query()
async def callback_handler(_, query: CallbackQuery):
    data = query.data
    user_name = query.from_user.first_name
    
    if data == "back_start":
        caption = (
            f"✨ **ʜᴇʏ** {user_name}!\n"
            f"✨ **ɪ ᴀᴍ** **ᴛᴜᴋᴋɪ ᴍᴜsɪᴄ ʙᴏᴛ 💖🕊️**\n\n"
            "🏆 **ʙᴇsᴛ ǫᴜᴀʟɪᴛỹ ғᴇᴀᴛᴜʀᴇs ɪɴsɪᴅᴇ**\n"
            "🛠️ **ᴍᴀᴅᴇ ʙʏ...** [ᴄᴏᴅᴇʀɴᴏᴠᴀ](https://t.me/CoderNova)\n\n"
            "ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴘ.\n"
            "ᴀsᴋ ʏᴏᴜʀ ᴅᴏᴜʙᴛs ᴀᴛ [sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ](" + SUPPORT_CHAT + ")\n\n"
            "ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : `/`"
        )
        await query.message.edit_caption(caption=caption, reply_markup=get_start_keyboard())
        
    elif data == "help_menu":
        help_text = "✨ ᴛᴜᴋᴋɪ ᴍᴜsɪᴄ ʜᴇʟᴘ ᴅᴇsᴋ ✨\n\nᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴛᴏ ᴇxᴘʟᴏʀᴇ ᴀʟʟ ᴀᴠᴀɪʟᴀʙʟᴇ ᴍᴜsɪᴄ ᴍᴏᴅᴜʟᴇs ᴀɴᴅ ɢᴜɪᴅᴇs."
        await query.message.edit_caption(caption=help_text, reply_markup=get_help_keyboard())
        
    elif data == "guide_menu":
        guide_text = (
            "📖 **ɢᴜɪᴅᴇ - ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛᴜᴋᴋɪ ᴍᴜsɪᴄ**\n\n"
            "𝟷. ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴡɪᴛʜ ᴀᴅᴍɪɴ ᴘᴇʀᴍɪssɪᴏɴs.\n"
            "𝟸. sᴛᴀʀᴛ ᴀ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ɪɴsɪᴅᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ.\n"
            "𝟹. ᴜsᴇ `/play [sᴏɴɢ ɴᴀᴍᴇ]` ᴛᴏ sᴛʀᴇᴀᴍ ʜɪɢʜ-ǫᴜᴀʟɪᴛʏ ᴀᴜᴅɪᴏ.\n"
            "𝟺. ᴜsᴇ `/skip` ᴏʀ `/pause` ᴛᴏ ᴄᴏɴᴛʀᴏʟ ᴍᴇᴅɪᴀ sᴛʀᴇᴀᴍs sᴇᴀᴍʟᴇssʟʏ."
        )
        await query.message.edit_caption(caption=guide_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_start")]]))

    elif data == "cmd_admin":
        txt = "🛡️ **ᴀheaderɴ ᴄᴏᴍᴍᴀɴᴅs:**\n\n• `/pause` - ᴘᴀᴜsᴇ ᴄᴜʀʀᴇɴᴛ sᴛʀᴇᴀᴍ\n• `/resume` - ʀᴇsᴜᴍᴇ ᴘᴀᴜsᴇᴅ sᴛʀᴇᴀᴍ\n• `/skip` - sᴋɪᴘ sᴏɴɢ\n• `/stop` - sᴛᴏᴘ sᴛʀᴇᴀᴍ"
        await query.message.edit_caption(caption=txt, reply_markup=get_back_keyboard())
        
    elif data == "cmd_auth":
        txt = "🔐 **ᴀᴜᴛʜ ᴄᴏᴍᴍᴀɴᴅs:**\n\n• `/auth` - ᴀᴜᴛʜᴏʀɪᴢᴇ ᴜsᴇʀ\n• `/unauth` - ʀᴇᴍᴏᴠᴇ ᴀᴜᴛʜᴏʀɪᴢᴀᴛɪᴏɴ\n• `/authusers` - ʟɪsᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀs"
        await query.message.edit_caption(caption=txt, reply_markup=get_back_keyboard())
        
    elif data == "cmd_cplay":
        txt = "🎛️ **ᴄ-ᴘʟᴀʏ ᴄᴏᴍᴍᴀɴᴅs:**\n\n• `/cplay` - ᴄʜᴀɴɴᴇʟ ᴘʟᴀʏ sᴛʀᴇᴀᴍ\n• `/cplay_list` - sʜᴏᴡ sᴛʀᴇᴀᴍ ǫᴜᴇᴜᴇ ɪɴ ᴄʜᴀɴɴᴇʟ"
        await query.message.edit_caption(caption=txt, reply_markup=get_back_keyboard())
        
    elif data == "cmd_loop":
        txt = "🔄 **ʟᴏᴏᴘ ᴄᴏᴍᴍᴀɴᴅs:**\n\n• `/loop [𝟷-𝟻]` - ʀᴇᴘᴇᴀᴛ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ sᴏɴɢ\n• `/loop disable` - ᴛᴜʀɴ ᴏғғ ʟᴏᴏᴘ ᴍᴏᴅᴇ"
        await query.message.edit_caption(caption=txt, reply_markup=get_back_keyboard())
        
    elif data == "cmd_play":
        txt = "▶️ **ᴘʟᴀʏ ᴄᴏᴍᴍᴀɴᴅs:**\n\n• `/play [sᴏɴɢ ɴᴀᴍᴇ]` - sᴛʀᴇᴀᴍ ᴀᴜᴅɪᴏ\n• `/vplay [ᴠɪᴅᴇᴏ ɴᴀᴍᴇ]` - sᴛʀᴇᴀᴍ ᴠɪᴅᴇᴏ\n• `/playlist` - sʜᴏᴡ ᴄᴜʀʀᴇɴᴛ ǫᴜᴇᴜᴇ"
        await query.message.edit_caption(caption=txt, reply_markup=get_back_keyboard())
        
    elif data == "cmd_shuffle":
        txt = "🔀 **sʜᴜғғʟᴇ ᴄᴏᴍᴍᴀɴᴅs:**\n\n• `/shuffle` - sʜᴜғғʟᴇ ǫᴜᴇᴜᴇ ɪᴛᴇᴍs\n• `/queue` - sʜᴏᴡ sʜᴜғғʟᴇᴅ ᴏʀᴅᴇʀ"
        await query.message.edit_caption(caption=txt, reply_markup=get_back_keyboard())
        
    elif data == "cmd_seek":
        txt = "⏩ **sᴇᴇᴋ ᴄᴏᴍᴍᴀɴᴅs:**\n\n• `/seek [ᴅᴜʀᴀᴛɪᴏɴ]` - sᴇᴇᴋ sᴛʀᴇᴀᴍ ғᴏʀᴡᴀʀᴅ\n• `/seekback [ᴅᴜʀᴀᴛɪᴏɴ]` - sᴇᴇᴋ ʙᴀᴄᴋᴡᴀʀᴅ"
        await query.message.edit_caption(caption=txt, reply_markup=get_back_keyboard())
        
    elif data == "cmd_speed":
        txt = "⚡ **sᴘᴇᴇᴅ ᴄᴏᴍᴍᴀɴᴅs:**\n\n• `/speed [𝟶.𝟻x-𝟸.𝟶x]` - sᴇᴛ ᴀᴜᴅɪᴏ ᴘʟᴀʏʙᴀᴄᴋ sᴘᴇᴇᴅ"
        await query.message.edit_caption(caption=txt, reply_markup=get_back_keyboard())
        
    elif data == "cmd_extra":
        txt = "🔮 **ᴇxᴛʀᴀ ᴄᴏᴍᴍᴀɴᴅs:**\n\n• `/lyrics [ɴᴀᴍᴇ]` - sᴇᴀʀᴄʜ sᴏɴɢ ʟʏʀɪᴄs\n• `/song [ɴᴀᴍᴇ]` - ᴅᴏᴡɴʟᴏᴀᴅ ᴀᴜᴅɪᴏ ᴅɪʀᴇᴄᴛʟʏ"
        await query.message.edit_caption(caption=txt, reply_markup=get_back_keyboard())

# ==========================================
# 📢 10. PREMIUM MASSS BROADCASTS (SUDO ONLY)
# ==========================================
@bot.on_message(filters.command("broadcast") & filters.user(OWNER_USERNAME))
async def simple_broadcast(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("❌ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ.")
    
    await message.reply_text("⚡ **sᴛᴀʀᴛɪɴɢ ʙʀᴏᴀᴅᴄᴀsᴛ ᴛᴏ ᴜsᴇʀs & ɢʀᴏᴜᴘs...**")
    
    if users_col is not None:
        for u in users_col.find():
            try:
                await message.reply_to_message.copy(u["user_id"])
                await asyncio.sleep(0.3)
            except Exception:
                pass
                
    if groups_col is not None:
        for g in groups_col.find():
            try:
                await message.reply_to_message.copy(g["chat_id"])
                await asyncio.sleep(0.3)
            except Exception:
                pass
    
    await message.reply_text("✅ **ʙʀᴏᴀᴅᴄᴀsᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ᴄᴏᴍᴘʟᴇᴛᴇcompleted!**")

@bot.on_message(filters.command("broadcast_all") & filters.user(OWNER_USERNAME))
async def global_broadcast_all(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("❌ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ ᴀʟʟ.")
        
    await message.reply_text("🔥 **sᴛᴀʀᴛɪɴɢ ᴍᴀssɪᴠᴇ ɢʟᴏʙᴀʟ ʙʀᴏᴀᴅᴄᴀsᴛ (ᴡɪᴛʜ ᴘɪɴ + ᴀssɪsᴛᴀɴᴛ)...**")
    
    if users_col is not None:
        for u in users_col.find():
            try:
                m = await message.reply_to_message.copy(u["user_id"])
                await m.pin(disable_notification=False)
                await asyncio.sleep(0.3)
            except Exception:
                pass
                
    if groups_col is not None:
        for g in groups_col.find():
            try:
                m = await message.reply_to_message.copy(g["chat_id"])
                await m.pin(disable_notification=False)
                await asyncio.sleep(0.3)
            except Exception:
                pass
                
    await message.reply_text("✅ **ɢʟᴏʙᴀʟ ᴍᴀss ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇ!**")

# ==========================================
# 🚀 11. SYSTEM INITIATION TRIGGER
# ==========================================
if __name__ == "__main__":
    init_keep_alive()  # Live port integration for Render hosting platform
    bot.run()

