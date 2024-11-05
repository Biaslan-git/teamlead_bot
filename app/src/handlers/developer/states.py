from aiogram.fsm.state import StatesGroup, State


class Auth(StatesGroup):
    sending_auth_key = State()
