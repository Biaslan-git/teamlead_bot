from aiogram.types import Message

from config import ADMIN_ID
from db import manager
from db.models import Status
from handlers.developer import keyboards
from handlers.utils import get_developers_string


async def send_my_projects_list(message: Message, **kwargs):
    projects = await manager.get_developer_current_projects_by_user_id(message.from_user.id)
    
    if projects:
        msg_text = '\n\n'.\
        join([f'/detail_my_project{x.id}\nНазвание: {x.title}\nЦена: ${x.price}\nСтатус: {x.status.value}' for x in projects])
    else:
        msg_text = 'Заказов нет. При появлении нового заказа вам придет уведомление'
    await message.answer(msg_text, **kwargs)

async def take_project(callback, project_id, developer_id):
    project = await manager.get_project_by_id(project_id)
    if len(project.developers) < project.developer_count and project.status not in (Status.completed, Status.canceled):
        project, developer = await manager.add_project_to_developer(project.id, developer_id)
        await send_project_take_notify_to_admin(callback.message, project)
        await callback.message.answer(f'Вы взяли заказ: {project.title}')
    else:
        await callback.message.delete()
        await callback.message.answer(f'Некорректный ввод')


def get_developer_name(message: Message):
    return '@'+message.from_user.username if message.from_user.username else message.from_user.first_name

async def complete_project(message: Message, project_id):
    project = await manager.change_project_status(project_id, Status.completed)
    if project:
        await send_to_admin(message, f'Разработчик {get_developer_name(message)} изменил статус заказа «{project.title}» на: {project.status.value}')
    else:
        await message.answer('Что-то пошло не так')


async def send_my_project_detail(message: Message, developer_user_id: int, project_id: int):
    dev_projects = await manager.get_developer_projects_by_user_id(developer_user_id)
    project = [project for project in dev_projects if project.id==project_id][0] if dev_projects else None
    if not project:
        await message.answer('Заказа с таким id не существует')
        return 

    developers = await manager.get_project_developers(project_id)
    developers_string = await get_developers_string(developers)


    text = f'Название: {project.title}\n'\
        f'Описание: {project.description}\n'\
        f'Стоимость: ${project.price}\n'\
        f'Статус: {project.status.value}\n'\
        f'Создан: {project.created}\n'\
        f'Обновлен: {project.updated}\n'\
        f'Взят: {project.taken_at or 'Еще не взят'}\n'\
        f'Разработчики: {developers_string or 'Нет'}'

    await message.answer(text, reply_markup=keyboards.get_project_detail_kb(project.id), parse_mode=None)
async def auth_developer(message):
    developer = await manager.add_developer(
        message.chat.id, 
        message.from_user.username, 
        message.from_user.first_name
    )
    await send_auth_notify_to_admin(message, developer)
    await message.answer('Вы успешно авторизовались', reply_markup=keyboards.kb_view_projects)

async def send_to_admin(message: Message, text: str):
    await message.bot.send_message(ADMIN_ID, text)

async def send_project_take_notify_to_admin(message, project):
    user = message.from_user
    developer_name = '@'+user.username if user.username else user.first_name
    text = f'Разработчик {developer_name} взял заказ «{project.title}»'
    await send_to_admin(message, text)

async def send_auth_notify_to_admin(message: Message, developer):
    developer_name = '@'+developer.username if developer.username else developer.first_name
    text = f'Добавлен новый разработчик: {developer_name}'
    await send_to_admin(message, text)
