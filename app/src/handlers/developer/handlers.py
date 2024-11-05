from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram import F

from db.manager import get_developer_by_user_id, get_auth_key, get_project_by_id
from handlers.developer import keyboards
from handlers.developer.states import *
from handlers.developer.utils import auth_developer, send_my_projects_list, send_my_project_detail, complete_project, take_project
from handlers.developer.filters import AuthDeveloperFilter

router = Router()

@router.message(AuthDeveloperFilter(), lambda msg: msg.text == 'Мои заказы')
async def my_projects(message: Message):
    await send_my_projects_list(message)

@router.message(AuthDeveloperFilter(), lambda msg: msg.text.startswith('/detail_my_project'))
async def project_detail(message: Message):
    project_id = message.text.strip('/detail_my_project')
    if project_id.isdigit():
        await send_my_project_detail(message, message.from_user.id, int(project_id))
    else:
        await message.answer('Некорректный ввод')

@router.callback_query(F.data.startswith('complete_project'))
async def complete_project_cb(callback: CallbackQuery):
    try:
        project_id = int(callback.data.strip('complete_project'))
        await complete_project(callback.message, project_id)
    except (TypeError, ValueError):
        await callback.message.answer('Некорректный ввод')
    await callback.answer()
    await callback.message.delete()
    

@router.callback_query(F.data.startswith('take_project'))
async def take_project_cmd(callback: CallbackQuery):
    project_id = callback.data.strip('take_project')
    developer_id = callback.from_user.id
    if project_id.isdigit():
        await take_project(callback, int(project_id), developer_id)
    await callback.answer()


@router.message(StateFilter(None), Command('auth'))
async def auth(message: Message, state: FSMContext):
    if await get_developer_by_user_id(message.chat.id):
        await message.answer('Текст для авторизованных разработчиков', reply_markup=keyboards.kb_view_projects)
    else:
        await message.answer('Отправьте ключ авторизации')
        await state.set_state(Auth.sending_auth_key)

@router.message(Auth.sending_auth_key)
async def check_auth_key(message: Message, state: FSMContext):
    auth_key = await get_auth_key()
    if message.text == auth_key:
        await auth_developer(message)
        await state.clear()
    else:
        await message.answer('Неверный ключ')
        await state.set_state(Auth.sending_auth_key)

