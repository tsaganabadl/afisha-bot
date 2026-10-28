from aiogram.fsm.state import State, StatesGroup

class SearchStates(StatesGroup):
    choosing_category = State()
    choosing_date = State()
    choosing_price = State()
    viewing_results = State()
