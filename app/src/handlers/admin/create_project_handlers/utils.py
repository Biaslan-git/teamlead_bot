from aiogram.types import Message
from sqlalchemy.exc import IntegrityError

from db import manager
from db.models import Project
from handlers.admin.create_project_handlers.keyboards import get_take_project_kb


async def create_and_send_out_project(message, user_data):
    project = await manager.create_project(
        title=user_data['title'],
        description=user_data['description'],
        price=user_data['price'],
        developer_count=user_data['developer_count']
    )
    developers = await send_project_to_developers(message, project)
    developers_string = f'Разработчики получившие уведомление о заказе:\n'\
        +f'{'\n'.join(developers) or 'Нет свободных разработчиков'}'

    await message.answer('Заказ успешно создан')
    await message.answer(developers_string)


async def send_project_to_developers(message: Message, project: Project) -> list[str]:
    developers = await manager.get_developers_to_take_project()

    text = f'Новый заказ!\n'\
        f'Название: {project.title}\n'\
        f'Описание: {project.description}\n'\
        f'Стоимость: ${project.price}\n'

    getted_developers_list = []
    for developer in developers:
        await message.bot.send_message( # type: ignore
            developer.user_id,  # type: ignore
            text, 
            reply_markup=get_take_project_kb(project.id) # type: ignore
        )
        developer_name = '@'+developer.username if developer.username else developer.first_name
        getted_developers_list.append(developer_name)
    return getted_developers_list

