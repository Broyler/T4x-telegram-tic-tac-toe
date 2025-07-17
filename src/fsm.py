from aiogram.fsm.state import StatesGroup, State


class TState(StatesGroup):
    selecting_move = State()
    observing = State()
    invites = State()
