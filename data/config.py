from environs import Env

env = Env()
env.read_env()

# Dajngo 
BOT_TOKEN = env.str("BOT_TOKEN")
# print(BOT_TOKEN)
SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.str("DEBUG", default=False)

PG_USER_NAME = env.str("PG_USER_NAME")
PG_DB_NAME = env.str("PG_DB_NAME")
PG_PASSWORD = env.str("PG_PASSWORD")
PG_HOST = env.str("PG_HOST")
PG_PORT = env.str("PG_PORT")

# # Aiogram bot
ADMIN = env.list("ADMIN")
# print(ADMIN)
