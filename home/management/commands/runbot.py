import asyncio
from django.core.management.base import BaseCommand
from aiogram_bot.app import main

class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **kwargs):
        asyncio.run(main())