from aiogram.types import Message, CallbackQuery

from db import manager
from db.models import DeveloperSpecialties, Developer
from handlers.admin.developer_operations_handlers.keyboards import get_developer_details_kb


async def send_developer_detail(message: Message, developer_id: int):
    developer = await manager.get_developer_by_id(developer_id)
    if not developer: 
        await message.answer('Разработчика с таким id не существует')
        return 

    text = await get_developer_detail_text(developer)

    await message.answer(text, reply_markup=get_developer_details_kb(developer), parse_mode=None)

async def change_developer_specialty(callback: CallbackQuery, developer_id):
    new_developer = await manager.change_developer_specialty(
        developer_id, # type: ignore
    )
    if new_developer:
        developer_detail_text = await get_developer_detail_text(new_developer)
        await callback.message.edit_text( # type: ignore
            developer_detail_text,
            reply_markup=get_developer_details_kb(new_developer)
        )


async def get_developer_detail_text(developer: Developer) -> str:
    projects_string = await get_projects_string(developer.projects)
    text = f'Имя: {get_developer_name(developer)}\n'\
        f'Специализация: {developer.specialty.value}\n'\
        f'Текущие проекты: {projects_string or 'Нет'}'
    return text


async def get_projects_string(projects):
    if projects:
        return ' | '.join([f'«{proj.title}»' for proj in projects])
    else:
        return ''


def get_developer_name(developer):
    return '@' + developer.username if developer.username else developer.first_name

