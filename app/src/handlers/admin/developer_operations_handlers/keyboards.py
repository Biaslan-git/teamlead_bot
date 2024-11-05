from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db import manager

def get_developer_details_kb(developer):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'Специализация: {developer.specialty.value}', callback_data=f'change_developer_specialty{developer.id}')],
        [InlineKeyboardButton(text='Удалить', callback_data=f'delete_developer{developer.id}')]
    ])
    return kb
