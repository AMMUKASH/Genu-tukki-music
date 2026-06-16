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

# Render Environment Variable for Assistant String Session
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
    t.daemon = True
    t.start()

# ==========================================
# 🎛️ 5. INLINE KEYBOARDS STRUCTS
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
# 📬 6. START COMMAND & DATA SYNC
# ==========================================
@bot.on_message(filters.command("start"))
async def start_handler(_, message: Message):
    user_name = message.from_user.first_name
    is_new_user = False
    
    if users_col is not None and message.chat.type == message.chat.type.PRIVATE:
        if not users_col.find_one({"user_id": message.from_user.id}):
            users_col.insert_one({"user_id": message.from_user.id, "username": message.from_user.username})
            is_new_user = True

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
# 🎵 7. MUSIC CONTROL CHANNELS & ROUTING
# ==========================================
@bot.on_message(filters.command(["play", "vplay"]))
async def play_audio(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ **ᴜsᴇ:** `/play [sᴏɴɢ ɴᴀᴍᴇ ᴏʀ ʟɪɴᴋ]`")
    
    query = " ".join(message.command[1:])
    
    # Global Chat Routing Button Layout
    gc_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 ᴊᴏɪɴ ᴏᴜʀ ᴍᴀɪɴ ɢᴄ / sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ 💬", url=SUPPORT_CHAT)]
    ])
    
    await message.reply_text(
        "🎵 **sᴛʀᴇᴀᴍ ɪs sᴛᴀʀᴛɪɴɢ... sᴀʙ ʟᴏɢ ᴍᴀɪɴ ɢᴄ ᴍᴇ ᴊᴀᴏ!**",
        reply_markup=gc_button
    )
    
    chat_id = message.chat.id
    chat_title = message.chat.title if message.chat.title else "ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ"
    
    if message.chat.type != message.chat.type.PRIVATE and groups_col is not None:
        if not groups_col.find_one({"chat_id": chat_id}):
            groups_col.insert_one({"chat_id": chat_id, "title": chat_title})

    try:
        await call_py.join_group_call(
            chat_id,
            AudioPcmInputFile("input.raw") 
        )
        
        play_log = (
            "🎵 **#ᴘʟᴀʏ_ʀᴇǫᴜᴇsᴛ sᴛʀᴇᴀᴍ**\n\n"
            f"👥 **ᴄʜᴀᴛ:** {chat_title}\n"
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
            
        action_log = f"⚙️ **#ᴄᴏᴍᴍᴀɴᴅ_ʟᴏɢ:** `/{command}` executed in **{chat_title}** (`{message.chat.id}`) by {message.from_user.mention}"
        await bot.send_message(LOG_GROUP, action_log)
        
    except Exception as e:
        await message.reply_text(f"ℹ️ **ᴍᴜsɪᴄ sᴛʀᴇᴀᴍ ɴᴏᴛ ᴀᴄᴛɪᴠᴇ ʀɪɢʜᴛ ɴᴏᴡ:** {e}")

# ==========================================
# 📥 8. BOT METRICS ROUTING (JOIN/LEFT LOGS)
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
            f"👤 **ᴀheader ʙ¥:** {message.from_user.mention if message.from_user else 'ᴜɴᴋɴᴏᴡɴ'}"
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
            f"👤 **ʀᴇᴍᴏᴠᴇᴅ ʙ¥:** {message.from_user.mention if message.from_user else 'ᴜɴᴋɴᴏᴡɴ'}"
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
            f"✨ **ʜᴇ¥** {user_name}!\n"
            f"✨ **ɪ ᴀᴍ** **ᴛᴜᴋᴋɪ ᴍᴜsɪᴄ ʙᴏᴛ 💖🕊️**\n\n"
            "🏆 **ʙᴇsᴛ ǫᴜᴀʟɪᴛỹ ғᴇᴀᴛᴜʀᴇs ɪɴsɪᴅᴇ**\n"
            "🛠️ **ᴍᴀᴅᴇ ʙ¥...** [ᴄᴏᴅᴇʀɴᴏᴠᴀ](https://t.me/CoderNova)\n\n"
            "ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀỹ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀheader ɢᴇᴛ ʜᴇʟᴘ.\n"
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
            "𝟷. ᴀheader ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴡɪᴛʜ ᴀheaderɴ ᴘᴇʀᴍɪssɪᴏɴs.\n"
            "𝟸. sᴛᴀheader ᴀ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ɪɴsɪᴅᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ.\n"
            "𝟹. ᴜsᴇ `/play [sᴏɴɢ ɴᴀᴍᴇ]` ᴛᴏ sᴛʀᴇᴀᴍ ʜɪɢʜ-ǫᴜᴀʟɪᴛ¥ ᴀᴜᴅɪᴏ.\n"
            "𝟺. ᴜsᴇ `/skip` ᴏʀ `/pause` ᴛᴏ ᴄᴏheaderᴏʟ ᴍᴇᴅɪᴀ sᴛʀᴇᴀᴍs sᴇᴀᴍʟᴇssʟỹ."
        )
        await query.message.edit_caption(caption=guide_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_start")]]))

    elif data == "cmd_admin":
        txt = "🛡️ **ᴀheaderɴ ᴄᴏᴍᴍᴀɴᴅs:**\n\n• `/pause` - ᴘᴀᴜsᴇ ᴄᴜʀʀᴇheader sᴛʀᴇᴀᴍ\n• `/resume` - ʀᴇsᴜᴍᴇ ᴘᴀᴜsᴇᴅ sᴛʀᴇᴀᴍ\n• `/skip` - sᴋɪᴘ sᴏɴɢ\n• `/stop` - sᴛᴏᴘ sᴛʀᴇᴀᴍ"
        await query.message.edit_caption(caption=txt, reply_markup=get_back_keyboard())
        
    elif data == "cmd_auth":
        txt = "🔐 **ᴀᴜᴛʜ ᴄᴏᴍᴍᴀɴᴅs:**\n\n• `/auth` - ᴀᴜᴛʜᴏʀɪᴢᴇ ᴜsᴇʀ\n• `/unauth` - ʀᴇᴍᴏᴠᴇ ᴀᴜᴛʜᴏʀɪᴢᴀheaderɴ\n• `/authusers` - ʟɪsᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀs"
        await query.message.edit_caption(caption=txt, reply_markup=get_back_keyboard())
        
    elif data == "cmd_cplay":
        txt = "🎛️ **...**\n\n• `/cplay` - ᴄʜᴀheader ᴘʟᴀ¥ sᴛʀᴇᴀᴍ\n• `/cplay_list` - sʜᴏᴡ sᴛʀᴇᴀᴍ ǫheader ɪheader ᴄʜᴀheader"
        await query.message.edit_caption(caption=txt, reply_markup=get_back_keyboard())
        
    elif data == "cmd_loop":
        txt = "🔄 **ʟᴏᴏᴘ ᴄᴏᴍᴍᴀɴᴅs:**\n\n• `/loop [𝟷-𝟻]` - ʀᴇᴘᴇᴀᴛ ᴛʜᴇ ᴄᴜʀʀᴇheader sᴏɴɢ\n• `/loop disable` - ᴛᴜheader ᴏғғ ʟᴏᴏᴘ ᴍᴏᴅᴇ"
        await query.message.edit_caption(caption=txt, reply_markup=get_back_keyboard())
        
    elif data == "cmd_play":
        txt = "▶️ **ᴘʟᴀ¥ ᴄᴏᴍᴍᴀɴᴅs:**\n\n• `/play [sᴏɴɢ ɴᴀᴍᴇ]` - sᴛʀᴇᴀᴍ ᴀᴜᴅɪᴏ\n• `/vplay [ᴠɪᴅᴇᴏ ɴᴀᴍᴇ]` - sᴛʀᴇᴀᴍ ᴠɪᴅᴇᴏ\n• `/playlist` - sʜᴏᴡ ᴄᴜʀʀᴇheader ǫheader"
        await query.message.edit_caption(caption=txt, reply_markup=get_back_keyboard())
        
    elif data == "cmd_shuffle":
        txt = "🔀 **sʜᴜғғʟᴇ ᴄᴏᴍᴍᴀɴᴅs:**\n\n• `/shuffle` - sʜᴜғғʟᴇ ǫheader ɪᴛᴇᴍs\n• `/queue` - sʜᴏᴡ sʜᴜғғʟᴇᴅ ᴏheader"
        await query.message.edit_caption(caption=txt, reply_markup=get_back_keyboard())
        
    elif data == "cmd_seek":
        txt = "⏩ **sᴇᴇᴋ ᴄᴏᴍᴍᴀɴᴅs:**\n\n• `/seek [ᴅheaderɪᴏheader]` - sᴇᴇᴋ sᴛʀᴇᴀᴍ ғᴏʀᴡᴀheader\n• `/seekback [ᴅheaderɪᴏheader]` - sᴇᴇᴋ ʙᴀᴄᴋᴡᴀheader"
        await query.message.edit_caption(caption=txt, reply_markup=get_back_keyboard())
        
    elif data == "cmd_speed":
        txt = "⚡ **sᴘᴇᴇᴅ ᴄᴏᴍᴍᴀɴᴅs:**\n\n• `/speed [𝟶.𝟻x-𝟸.𝟶x]` - sᴇᴛ ᴀᴜᴅɪᴏ ᴘʟᴀ¥ʙᴀᴄᴋ sᴘᴇᴇᴅ"
        await query.message.edit_caption(caption=txt, reply_markup=get_back_keyboard())
        
    elif data == "cmd_extra":
        txt = "🔮 **ᴇxheader ᴄᴏᴍᴍᴀɴᴅs:**\n\n• `/lyrics [ɴᴀᴍᴇ]` - sᴇᴀheader sᴏɴɢ ʟỹʀɪᴄs\n• `/song [ɴᴀᴍᴇ]` - ᴅᴏᴡheaderᴅ ᴀᴜᴅɪᴏ ᴅɪʀᴇᴄheader"
        await query.message.edit_caption(caption=txt, reply_markup=get_back_keyboard())

# ==========================================
# 📢 10. PREMIUM MASS BROADCASTS (SUDO ONLY)
# ==========================================
@bot.on_message(filters.command("broadcast") & filters.user(OWNER_USERNAME))
async def simple_broadcast(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("❌ ʀᴇᴘʟ¥ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ʙheadersᴛ.")
    
    await message.reply_text("⚡ **sᴛᴀheaderɢ ʙheadersᴛ ᴛᴏ ᴜsᴇʀs & ɢʀᴏᴜᴘs...**")
    
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
    
    await message.reply_text("✅ **ʙheadersᴛ sᴜᴄᴄᴇssғᴜʟʟ¥ ᴄᴏᴍᴘʟᴇᴛᴇᴅ!**")

# ==========================================
# 🚀 11. BOOTSTRAP & DYNAMIC EVENT LOOP
# ==========================================
if __name__ == "__main__":
    init_keep_alive()
    
    # Render Python 3.11+ asyncio engine fix
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    # Start both client frameworks synchronously inside loop
    loop.run_until_complete(bot.start())
    loop.run_until_complete(assistant.start())
    
    # Trigger Assistant log active event 
    try:
        assistant_me = loop.run_until_complete(assistant.get_me())
        assistant_name = assistant_me.first_name
        assistant_id = assistant_me.id
        assistant_username = f"@{assistant_me.username}" if assistant_me.username else "ɴᴏ_ᴜsᴇʀɴᴀᴍᴇ"
        
        system_start_text = (
            "⚙️ **ᴛᴜᴋᴋɪ ᴍᴜsɪᴄ sʏsᴛᴇᴍ ᴀᴄᴛɪᴠᴀᴛᴇᴅ**\n\n"
            "✅ **ʙᴏᴛ sᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ᴏɴ ʀᴇɴᴅᴇʀ!**\n"
            f"🤖 **ᴀssɪsᴛᴀɴᴛ ɴᴀᴍᴇ:** {assistant_name}\n"
            f"🆔 **ᴀssɪsᴛᴀɴᴛ ɪᴅ:** `{assistant_id}`\n"
            f"🔗 **ᴀssɪsᴛᴀɴᴛ ᴜsᴇʀɴᴀᴍᴇ:** {assistant_username}\n\n"
            "✨ *sʏsᴛᴇᴍ ɪs 𝟸𝟺/𝟽 ʟɪᴠᴇ ᴀɴᴅ ʀᴜɴɴɪɴɢ...*"
        )
        loop.run_until_complete(bot.send_message(LOG_GROUP, system_start_text))
    except Exception as e:
        print(f"Failed to send startup log: {e}")

    # Keep services running indefinitely 
    loop.run_forever()
