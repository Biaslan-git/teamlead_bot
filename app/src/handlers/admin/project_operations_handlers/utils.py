from aiogram.types import Message, CallbackQuery

from db import manager
from db.models import Project
from handlers.utils import get_developers_string
from handlers.admin.project_operations_handlers.keyboards import get_project_detail_kb,\
    get_project_pagination_kb
from handlers.admin.project_operations_handlers.message_texts import project_short_desc


async def send_projects_page(message: Message, page: int = 1, edit_text: bool = False):
    # projects = await manager.get_projects()
    projects = await manager.get_projects_by_page(page)
    
    if projects:
        msg_text = ''.join([project_short_desc.format(
            project_id=project.id,
            project_title=project.title,
            project_price=project.price,
            project_status=project.status.value,
        ) for project in projects])
    else:
        msg_text = 'Заказов нет'
    
    if edit_text:
        await message.edit_text(msg_text, reply_markup=await get_project_pagination_kb(page))
    else:
        await message.answer(msg_text, reply_markup=await get_project_pagination_kb(page))



async def change_project_status(callback: CallbackQuery, project_id):
    new_project = await manager.change_project_status(
        project_id, # type: ignore
    )

    if new_project:
        project_detail_text = await get_project_detail_text(new_project)
        await callback.message.edit_text( # type: ignore
            project_detail_text,
            reply_markup=get_project_detail_kb(new_project)
        )


async def get_project_detail_text(project: Project):
    developers = await manager.get_project_developers(project.id) # type: ignore
    developers_string = await get_developers_string(developers)
    text = f'Название: {project.title}\n'\
        f'Описание: {project.description}\n'\
        f'Стоимость: ${project.price}\n'\
        f'Статус: {project.status.value}\n'\
        f'Создан: {project.created}\n'\
        f'Обновлен: {project.updated}\n'\
        f'Взят: {project.taken_at or 'Еще не взят'}\n'\
        f'Установленное количество разработчиков: {project.developer_count}\n'\
        f'Текущее количество разработчиков: {len(developers) if developers else 0}\n'\
        f'Разработчики: {developers_string or 'Нет разработчиков'}'
    return text
    
async def send_project_detail(message: Message, id: int):
    project = await manager.get_project_by_id(id)
    if not project: 
        await message.answer('Заказа с таким id не существует')
        return 


    text = await get_project_detail_text(project)

    await message.answer(text, reply_markup=get_project_detail_kb(project), parse_mode=None)
