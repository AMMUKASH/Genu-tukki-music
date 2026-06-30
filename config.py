import os

# Telegram API credentials
API_ID = int(os.getenv("API_ID", "38138069"))
API_HASH = os.getenv("API_HASH", "2ed313ebcc45cbcf65d1fc736ec71681")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8997247669:AAEhcPwhbtRwR3SxvVKsZU3bSnnS3RPO5xg")
STRING_SESSION = os.getenv("STRING_SESSION", "AQJF8NUAgBfq_JynQDTlV8Bw7YUi_5Xr8Y_0JWiGElK7XrAUyeBr9Iu87Heq8j3EZ42zuFbbJgv1RmgkNt0CErphSozbaL0sG8TYIm9RqPPYTRR3LmeNGkGkb")

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://misssqn_db_user:Nova01@cluster0.6xxsrwq.mongodb.net/?retryWrites=true&w=majority")

# Log group ID
LOG_GROUP = int(os.getenv("LOG_GROUP", "-1003947649552"))

# Owner and support info
OWNER = os.getenv("OWNER", "@CoderNova")
SUPPORT = os.getenv("SUPPORT", "https://t.me/Genu_Bot_Support/119")

# Bot username
BOT_USERNAME = os.getenv("BOT_USERNAME", "@Tukki_Music_Bot")
