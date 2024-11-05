from aiogram.filters import BaseFilter
from aiogram.types import Message
from config import ADMIN_ID


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.id == ADMIN_ID

class NotAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.id != ADMIN_ID



