from aiogram import Router
from aiogram.filters import Filter
from aiogram.types import Message
from asgiref.sync import sync_to_async
from user.models import CustomUser


class IsAdminFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        admin = await sync_to_async(CustomUser.objects.filter)(telegram_id=message.chat.id, is_staff=True)
        return await sync_to_async(admin.exists)()
    

