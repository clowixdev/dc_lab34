from hashlib import md5 as hash

from aiogram import F, Router, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from database.dbworker import get_user, add_user, add_user_pred
from database.msg import REPLIES
from loader import engine
# , model
# from scripts.predictor import recognize_picture
from states.states import Registration, Session, Login, Predict

router = Router()


@router.message(Command("start", "help"))
async def cmd_help(message: types.Message):
    print(message.from_user.id)
    await message.reply(REPLIES["help"])


@router.message(Command("register"))
async def cmd_register(message: types.Message, state: FSMContext):
    if (get_user(message.from_user.id, engine)):
        await message.reply(REPLIES["registration_already"])
        return
    else:
        await message.reply(REPLIES["register_start"])
        await state.set_state(Registration.entering_psw)


@router.message(Registration.entering_psw)
async def reg_enter_psw(message: types.Message, state: FSMContext):
    if (message.text.lower() == "стоп"):
        await message.reply(REPLIES["stop"])
        await state.set_state(Session.logged_in)

        return

    await state.update_data(psw_hash=hash(message.text.encode()).hexdigest())
    await message.reply(REPLIES["register_confirm"])
    await state.set_state(Registration.confirming_psw)


@router.message(Registration.confirming_psw)
async def reg_confirm_psw(message: types.Message, state: FSMContext):
    if (message.text.lower() == "стоп"):
        await message.reply(REPLIES["stop"])
        await state.set_state(Session.logged_in)

        return

    user_data = await state.get_data()
    if (user_data["psw_hash"] == hash(message.text.encode()).hexdigest()):
        add_user([message.from_user.id, user_data["psw_hash"]], engine)
        await message.reply(REPLIES["registration_completed"])
        await state.set_state(None)
    else:
        await message.reply(REPLIES["passwords_are_not_same"])
        await message.reply(REPLIES["register_confirm"])


@router.message(Command("login"))
async def cmd_login(message: types.Message, state: FSMContext):
    if (await state.get_state() == Session.logged_in):
        await message.reply(REPLIES["already_logged"])
        
        return
    
    if (get_user(message.from_user.id, engine) is None):
        await message.reply(REPLIES["not_registered"])
        return
    else:
        await message.reply(REPLIES["login_password"])
        await state.set_state(Login.entering_psw)


@router.message(Login.entering_psw)
async def log_enter_psw(message: types.Message, state: FSMContext):
    if (message.text.lower() == "стоп"):
        await message.reply(REPLIES["stop"])
        await state.set_state(None)

        return

    psw_hash = hash(message.text.encode()).hexdigest()
    cur_user_hash = get_user(message.from_user.id, engine).psw_hash
    if (psw_hash == cur_user_hash):
        await message.reply(REPLIES["logged_in"])
        await state.set_state(Session.logged_in)
    else:
        await message.reply(REPLIES["incorrect_psw"])


@router.message(Command("predict"))
async def cmd_predict(message: types.Message, state: FSMContext):
    if (await state.get_state() == Session.logged_in):
        await message.reply(REPLIES["predict_prompt"])
        await state.set_state(Predict.waiting_pic)
    else:
        await message.reply(REPLIES["not_logged"])


@router.message(Predict.waiting_pic)
async def predict_waiting_pic(message: types.Message, state: FSMContext, bot: Bot):
    if (message.text and message.text.lower() == "стоп"):
        await message.reply(REPLIES["stop"])
        await state.set_state(Session.logged_in)
        return
    elif (message.text):
        await message.reply(REPLIES["not_a_photo"])
        return
    if (message.photo):
        filename = f"./data/content/{message.from_user.id}.jpg"
        await bot.download(message.photo[-1], filename)
        await message.reply(REPLIES["is_predicting"])

        # answer, probability = recognize_picture(filename, model)
        answer, probability = 2, 1 
        match answer:
            case 0:
                await message.reply(REPLIES["is_bear"].format(
                    probability=(1 - int(probability)) * 100
                ))
            case 1:
                await message.reply(REPLIES["is_human"].format(
                    probability=probability * 100
                ))
            case _:
                await message.reply(REPLIES["error"])

        user = get_user(message.from_user.id, engine)
        add_user_pred(user.id, engine)

        await message.reply(REPLIES["predict_prompt"])

@router.message(Command("logout"))
async def cmd_logout(message: types.Message, state: FSMContext):
    if (await state.get_state() != Session.logged_in):
        await message.reply(REPLIES["not_logged"])
    else:
        await state.set_state(None)
        await message.reply(REPLIES["logout"])


@router.message(F)
async def no_cmd(message: types.Message):
    await message.reply(REPLIES["miss"])