from pyrogram import Client, filters

@Client.on_message(filters.command("auth"))
async def auth_user(client, message):
    await message.reply_text("✅ User authorized.")

@Client.on_message(filters.command("admin"))
async def admin_menu(client, message):
    await message.reply_text("👑 Admin menu loaded.")
