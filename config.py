import os

# Telegram API credentials
API_ID = int(os.getenv("API_ID", "38138069"))
API_HASH = os.getenv("API_HASH", "2ed313ebcc45cbcf65d1fc736ec71681")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8997247669:AAEhcPwhbtRwR3SxvVKsZU3bSnnS3RPO5xg")
STRING_SESSION = os.getenv("STRING_SESSION", "AQJF8NUAe1WySGfrc-qyyjlopoXBoTQty3jwIE0c31BTo3a5nJl_Kxyw35Iiv8lIE6vmoleR8ks5xyHucEAUd_2bpzMF5cprJcGl4RGsZOxF2-vmxFA2lXLzvaeAMCbQgL8fqGDNCzzeJ7htTWTVja0lte3xF7Tb2o-4jyVB-1VmxQ0vobZgcuGFTsjyR5fwmWw5NNw-jemRQAa1GyF_rU9nv6Z8z6HIZquIsFxMqjrAEAQWzVa5gKaBlP20tqZQI3cuL74du1WwOZv9bhSy4B45gfFflpraTgQOFZkoxZ2cDMnOxAniWB5WvM1E250QxV5AEGhFeIFfaIP66o5zCgaxHsrA9AAAAAH_hA2LAA")

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://misssqn_db_user:Nova01@cluster0.6xxsrwq.mongodb.net/?retryWrites=true&w=majority")

# Log group ID
LOG_GROUP = int(os.getenv("LOG_GROUP", "-1003947649552"))

# Owner and support info
OWNER = os.getenv("OWNER", "@CoderNova")
SUPPORT = os.getenv("SUPPORT", "https://t.me/NovaBot_Support")

# Bot username
BOT_USERNAME = os.getenv("BOT_USERNAME", "@Tukki_Music_Bot")
