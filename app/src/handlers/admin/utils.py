from aiogram.types import Message

from handlers.admin.keyboards import kb_main
from db.models import Status
from db import manager


async def send_main_menu(message: Message):
    developers = await manager.get_developers()
    developers_busy = [dev for dev in developers if dev.projects]
    developers_not_busy = [dev for dev in developers if not dev.projects]
    auth_key = await manager.get_auth_key()
    projects = await manager.get_projects()
    projects_in_dev = [proj for proj in projects if proj.status==Status.in_progress] # type:ignore
    projects_not_in_dev = [proj for proj in projects if proj.status==Status.pending] # type:ignore
    projects_completed = [proj for proj in projects if proj.status==Status.completed] # type:ignore
    projects_canceled = [proj for proj in projects if proj.status==Status.canceled] # type:ignore
    statistic_text = 'Общие данные: \n\n'\
        f'Всего разработчиков: {len(developers)}\n'\
        f'Занятых разработчиков: {len(developers_busy)}\n'\
        f'Свободных разработчиков: {len(developers_not_busy)}\n'\
        f'Ключ авторизации: {auth_key}\n\n'\
        f'Всего проектов: {len(projects)}\n'\
        f'Проектов в разработке: {len(projects_in_dev)}\n'\
        f'Ожидающих проектов: {len(projects_not_in_dev)}\n'\
        f'Завершенных проектов: {len(projects_completed)}\n'\
        f'Отменных проектов: {len(projects_canceled)}\n'\
        
    await message.answer(statistic_text, reply_markup=kb_main)



async def send_developers_list(message: Message, **kwargs):
    async def projects_count(developer_id):
        projects = await manager.get_developer_projects(developer_id)
        return len(projects) if projects else 0
    developers = await manager.get_developers()
    
    if developers:
        msg_text = '\n\n'\
            .join([f'/detail_developer{dev.id}\n'\
            +f'Имя: {get_developer_name(dev)}\n'\
            +f'Специализация: {dev.specialty.value}\n'\
            +f'Количество текущих проектов: {await projects_count(dev.id)}' for dev in developers])
    else:
        msg_text = 'Разработчиков нет'
    await message.answer(msg_text, **kwargs)

    
def get_developer_name(developer):
    return '@' + developer.username if developer.username else developer.first_name


async def get_projects_string(projects):
    if projects:
        return ' | '.join([f'«{proj.title}»' for proj in projects])
    else:
        return ''


