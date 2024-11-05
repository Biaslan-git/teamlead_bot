from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


kb_view_projects_btns = [
    [KeyboardButton(text='Мои заказы')],
]
kb_view_projects = ReplyKeyboardMarkup(keyboard=kb_view_projects_btns, resize_keyboard=True)


def get_project_detail_kb(project_id: int):
    kb_project_detail = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Выполнил', callback_data=f'complete_project{project_id}')]
    ])
    return kb_project_detail
