from aiogram.fsm.state import StatesGroup, State

class Registration(StatesGroup):
    entering_psw = State()
    confirming_psw = State()

class Login(StatesGroup):
    entering_psw = State()

class Predict(StatesGroup):
    waiting_pic = State()

class Session(StatesGroup):
    logged_in = State()