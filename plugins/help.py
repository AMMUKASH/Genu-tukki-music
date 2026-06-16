from pyrogram import Client, filters

HELP_TEXT = """
🎧 **Tukki Music Bot Commands**

/play [song/link] – Play music  
/cplay – Play in channel  
/loop [number] – Loop track  
/shuffle – Shuffle playlist  
/seek [seconds] – Seek track  
/speed [value] – Change speed  
/admin – Admin commands  
/auth – Authorize users  

✨ All commands work in **groups + private**.
"""

@Client.on_callback_query(filters.regex("help"))
async def help_menu(client, query):
    await query.message.edit_text(HELP_TEXT)
