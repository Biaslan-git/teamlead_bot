from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from handlers.admin.filters import AdminFilter
from db.manager import delete_project

from handlers.admin.project_operations_handlers.utils import send_project_detail,\
    change_project_status,\
    send_projects_page


router = Router()


@router.message(AdminFilter(), lambda msg: msg.text == 'Заказы')
async def projects_list_cmd(message: Message):
    await send_projects_page(message)


@router.callback_query(F.data.startswith('projects_page'))
async def projects_page_clbk(callback: CallbackQuery):
    page = int(callback.data.strip('projects_page'))
    await send_projects_page(callback.message, page, True)
    await callback.answer()



@router.message(AdminFilter(), lambda msg: msg.text.startswith('/detail_project'))
async def project_detail_cmd(message: Message):
    project_id = message.text.strip('/detail_project') # type: ignore
    if project_id.isdigit():
        await send_project_detail(message, int(project_id))
    else:
        await message.answer('Некорректный ввод')

@router.callback_query(F.data.startswith('delete_project'))
async def delete_project_clbk(callback_query: CallbackQuery):
    project_id = callback_query.data.strip('delete_project') # type: ignore
    if project_id.isdigit():
        await delete_project(int(project_id))
        await callback_query.message.answer('Заказ был удален') # type: ignore
    else:
        await callback_query.message.answer('Некорректный ввод') # type: ignore
    await callback_query.message.delete() # type: ignore
    await callback_query.answer()

@router.callback_query(F.data.startswith('change_status_project'))
async def change_status_clbk(callback: CallbackQuery):
    try:
        project_id = int(callback.data.strip('change_status_project')) # type: ignore
        print(f'{project_id=}')
        await change_project_status(callback, project_id)
    except (TypeError, ValueError):
        await callback.message.answer('Некорректный ввод') # type: ignore
        await callback.message.delete() # type: ignore
    await callback.answer()
