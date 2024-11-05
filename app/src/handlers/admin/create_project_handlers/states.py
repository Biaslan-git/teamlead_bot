from aiogram.fsm.state import StatesGroup, State


class CreateProject(StatesGroup):
    title = State()
    description = State()
    price = State()
    developer_count = State()
    
