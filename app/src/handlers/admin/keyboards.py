from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb_main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Создать заказ')],
    [KeyboardButton(text='Разработчики')],
    [KeyboardButton(text='Заказы')],
], resize_keyboard=True)

kb_developers = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Главная')],
    [KeyboardButton(text='Разработчики')],
    [KeyboardButton(text='Показать ключ авторизации')],
    [KeyboardButton(text='Обновить ключ авторизации')],
], resize_keyboard=True)


