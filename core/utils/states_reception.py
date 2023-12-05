from aiogram.fsm. state import StatesGroup, State

class StateReception(StatesGroup):
    first_state = State()
    second_state = State()
    third_state = State()
    four_state = State()

class StateCancelReception(StatesGroup):
    first_state = State()
    second_state = State()
    third_state = State()
    four_state = State()

class StateAllRecordings(StatesGroup):
    first_state = State()
    second_state = State()