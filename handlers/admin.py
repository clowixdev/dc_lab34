from aiogram import Router, types
from aiogram.filters import Command, CommandObject

from database.dbworker import get_all_users, delete_user, get_user, add_adm_user
from database.msg import REPLIES
from loader import engine
from scripts.decorators import admin_required

router = Router()

@router.message(Command("stats"))
@admin_required
async def adm_cmd_stats(message: types.Message):
    users = get_all_users(engine)
    users_msg = ""
    for user in users:
        users_msg += REPLIES["user_stat"].format(
            role="A👮🏻" if user.is_admin else "U👴🏻",
            id=user.id,
            predictions=user.pred_count
        )

    await message.reply(REPLIES["all_users"].format(users=users_msg))


@router.message(Command("rmuser"))
@admin_required
async def adm_cmd_rmuser(message: types.Message, command: CommandObject):    
    if command.args is None:
        await message.answer(REPLIES["no_args_rm"])
        return

    user = get_user(command.args, engine)
    if (user):
        delete_user(user.id, engine)
        await message.answer(REPLIES["delete_user"].format(id=command.args))
    else:
        await message.answer(REPLIES["incorrect_id"])


@router.message(Command("addadm"))
@admin_required
async def adm_cmd_addadm(message: types.Message, command: CommandObject):
    if command.args is None:
        await message.answer(REPLIES["no_args_add"])
        return

    user = get_user(command.args, engine)
    if (user):
        add_adm_user(user.id, engine)
        await message.answer(REPLIES["add_user"].format(id=command.args))
    else:
        await message.answer(REPLIES["incorrect_id"])