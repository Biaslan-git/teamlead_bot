from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,\
    InlineKeyboardMarkup, InlineKeyboardButton


kb_create_project = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Главная')],
], resize_keyboard=True)

kb_create_project_dev_count = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Главная')],
    [KeyboardButton(text='1'), KeyboardButton(text='2'), KeyboardButton(text='3')],
    [KeyboardButton(text='4'), KeyboardButton(text='5'), KeyboardButton(text='6')],
    [KeyboardButton(text='7'), KeyboardButton(text='8'), KeyboardButton(text='9')],
], resize_keyboard=True)

def get_take_project_kb(project_id: int):
    kb_take_project_btn = InlineKeyboardButton(text='Взять', callback_data=f'take_project{project_id}')
    kb_take_project = InlineKeyboardMarkup(inline_keyboard=[[kb_take_project_btn]])
    return kb_take_project

