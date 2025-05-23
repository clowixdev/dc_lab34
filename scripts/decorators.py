from typing import Callable, Any
from functools import wraps

from database.dbworker import get_user
from loader import engine
from database.msg import REPLIES

def admin_required(func: Callable) -> Any:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        user = get_user(args[0].from_user.id, engine)
        if (not user or not user.is_admin):
            await args[0].reply(REPLIES["insufficient_rights"])
            return
        return await func(*args, **kwargs)
    return wrapper