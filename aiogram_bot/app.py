import asyncio
import logging
import sys

# import handlers
from aiogram_bot.loader import dp, bot
from aiogram_bot.debt_sender import setup_scheduler
import aiogram_bot.handlers




async def main() -> None:
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.basicConfig(
    level=logging.INFO,  # Log darajasi: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Loglarni terminalga chiqarish
        # Agar faylga yozish istasangiz:
        # logging.FileHandler('bot.log')
    ],stream=sys.stdout)
    # logging.basicConfig(level=logging.WARNING) 
    print("Bot running ...")
    setup_scheduler()
    await dp.start_polling(bot)

