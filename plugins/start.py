from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config

@Client.on_message(filters.command("start"))
async def start(client, message):
    buttons = [
        [InlineKeyboardButton("➕ Add Me", url=f"https://t.me/{config.BOT_USERNAME}?startgroup=true")],
        [InlineKeyboardButton("👑 Owner", url="https://t.me/CoderNova")],
        [InlineKeyboardButton("🛠 Support", url=config.SUPPORT)],
        [InlineKeyboardButton("📜 Help & Commands", callback_data="help")],
        [InlineKeyboardButton("📖 Guide", callback_data="guide")]
    ]
    await message.reply_text(
        f"✨ Hey {message.from_user.mention}, Welcome to Tukki Music Bot 🎶\n"
        f"Enjoy nonstop music with stylish features!\n\n"
        f"Made with ❤️ by {config.OWNER}\nSupport: [Click Here]({config.SUPPORT})",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
