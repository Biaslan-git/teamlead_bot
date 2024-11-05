from aiogram.filters import BaseFilter
from aiogram.types import Message

from db import manager


class AuthDeveloperFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return bool(await manager.get_developer_by_user_id(message.chat.id))



