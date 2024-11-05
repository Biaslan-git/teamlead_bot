from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

from handlers.admin.filters import AdminFilter
from handlers.admin.keyboards import kb_developers
from handlers.admin.utils import send_main_menu, send_developers_list
from handlers.admin.create_project_handlers.handlers import router as router_create_project
from handlers.admin.developer_operations_handlers.handlers import router as router_developer_operations
from handlers.admin.project_operations_handlers.handlers import router as router_project_operations
from db import manager


router = Router()

router.include_router(router_create_project)
router.include_router(router_developer_operations)
router.include_router(router_project_operations)


@router.message(Command('admin'), AdminFilter())
@router.message(StateFilter(None), lambda message: message.text == 'Главная', AdminFilter())
async def admin_cmd(message: Message):
    await send_main_menu(message)


@router.message(lambda message: message.text == 'Разработчики', AdminFilter())
async def developers_cmd(message: Message):
    await send_developers_list(message, reply_markup=kb_developers)



@router.message(lambda message: message.text=='Показать ключ авторизации', AdminFilter())
async def get_auth_key(message: Message):
    auth_key = await manager.get_auth_key()
    await message.answer(f'Ключ авторизации: `{auth_key}`', parse_mode='markdown')


@router.message(lambda message: message.text=='Обновить ключ авторизации', AdminFilter())
async def update_auth_key(message: Message):
    auth_key = await manager.update_auth_key()
    await message.answer(f'Ключ авторизации: `{auth_key}`', parse_mode='markdown')

