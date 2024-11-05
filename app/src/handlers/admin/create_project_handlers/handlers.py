from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from handlers.admin.filters import AdminFilter
from handlers.admin.utils import send_main_menu
from handlers.admin.create_project_handlers.manager import get_project_by_title
from handlers.admin.create_project_handlers.utils import create_and_send_out_project
from handlers.admin.create_project_handlers.states import CreateProject
from handlers.admin.create_project_handlers.keyboards import kb_create_project,\
    kb_create_project_dev_count


router = Router()

@router.message(
    AdminFilter(), StateFilter(None),
    lambda message: message.text == 'Создать заказ')
async def create_project(message: Message, state: FSMContext):
    await message.answer('Отправьте название заказа', reply_markup=kb_create_project)
    await state.set_state(CreateProject.title)

@router.message(AdminFilter(), CreateProject.title, lambda message: bool(message.text))
async def create_project_title(message: Message, state: FSMContext):
    if message.text == 'Главная':
        await state.clear()
        await send_main_menu(message)
        return

    if not message.text: return

    project_by_title = await get_project_by_title(message.text)
    if project_by_title:
        await message.answer(
            'Заказ с таким названием уже существует. Попробуйте отправить другое название'
        )
    else:
        await state.update_data(title=message.text)
        await message.answer('Отправьте описание заказа')
        await state.set_state(CreateProject.description)


@router.message(AdminFilter(), CreateProject.description, lambda message: bool(message.text))
async def create_project_desc(message: Message, state: FSMContext):
    if message.text == 'Главная':
        await state.clear()
        await send_main_menu(message)
    else:
        await state.update_data(description=message.text)
        await message.answer('Отправьте стоимость заказа')
        await state.set_state(CreateProject.price)

@router.message(AdminFilter(), CreateProject.price, lambda message: bool(message.text))
async def create_project_price(message: Message, state: FSMContext):
    if message.text == 'Главная':
        await state.clear()
        await send_main_menu(message)
        return
    else:
        if message.text and message.text.isdigit():
            await state.update_data(price=int(message.text))
            await message.answer('Отправьте количество разработчиков', 
                                 reply_markup=kb_create_project_dev_count)
            await state.set_state(CreateProject.developer_count)
        else:
            await message.answer('Некорректный ввод. Попробуйте еще раз')

@router.message(AdminFilter(), CreateProject.developer_count, lambda message: bool(message.text))
async def create_project_count(message: Message, state: FSMContext):
    if message.text == 'Главная':
        await state.clear()
        await send_main_menu(message)
        return
    if message.text and message.text.isdigit() and int(message.text)>0:
        await state.update_data(developer_count=int(message.text))
        user_data = await state.get_data()

        await create_and_send_out_project(message, user_data)

        await state.clear()
        await send_main_menu(message)

    else:
        await message.answer('Некорректный ввод. Попробуйте еще раз')
