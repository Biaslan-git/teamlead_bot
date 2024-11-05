from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from handlers.admin.filters import AdminFilter
from handlers.admin.developer_operations_handlers.utils import change_developer_specialty, send_developer_detail
from db.manager import delete_developer


router = Router()


@router.message(AdminFilter(), lambda msg: msg.text.startswith('/detail_developer'))
async def developer_detail(message: Message):
    try:
        developer_id = int(message.text.strip('/detail_developer')) # type: ignore
        await send_developer_detail(message, developer_id)
    except (TypeError, ValueError):
        await message.answer('Некорректный ввод')

@router.callback_query(F.data.startswith('change_developer_specialty'))
async def change_developer_specialty_clbk(callback: CallbackQuery):
    if not callback.data: return
    developer_id = int(callback.data.strip('change_developer_specialty'))
    await change_developer_specialty(callback, developer_id)

    await callback.answer()
    


@router.callback_query(F.data.startswith('delete_developer'))
async def delete_developer_clbk(callback_query: CallbackQuery):
    developer_id = callback_query.data.strip('delete_developer') # type: ignore
    if developer_id.isdigit():
        await delete_developer(int(developer_id))
        await callback_query.message.answer('Разработчик был удален') # type: ignore
    else:
        await callback_query.message.answer('Некорректный ввод') # type: ignore
    await callback_query.message.delete() # type: ignore
    await callback_query.answer()
