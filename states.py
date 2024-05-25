from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    name = State()
    activity = State()
    goal = State()
    age = State()
    sex = State()
    height = State()
    weight = State()
    do_save = State()

class main_states(StatesGroup):
    form = State()
    exercise = State()
    meal = State()