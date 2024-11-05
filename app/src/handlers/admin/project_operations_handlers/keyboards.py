from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db.manager import get_projects_count


async def get_project_pagination_kb(cur_page: int):
    pag_btns = []
    projects_count = await get_projects_count()
    if cur_page>1:
        pag_btns.append(
            InlineKeyboardButton(text='<', callback_data=f'projects_page{cur_page-1}')
        )


    if cur_page*5<projects_count:
        pag_btns.append(
            InlineKeyboardButton(text='>', callback_data=f'projects_page{cur_page+1}')
        )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        pag_btns
    ])
    return kb


def get_project_detail_kb(project):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f'Статус: {project.status.value}', 
            callback_data=f'change_status_project{project.id}'
        )],
        [InlineKeyboardButton(text='Удалить', callback_data=f'delete_project{project.id}')]
    ])
    return kb
