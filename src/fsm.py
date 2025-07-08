from aiogram.fsm.state import StatesGroup, State


class PlayingState(StatesGroup):
    selecting_move = State()
    observing = State()
