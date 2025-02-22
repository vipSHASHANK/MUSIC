from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message
from config import *
from SHUKLAMUSIC import app
from SHUKLAMUSIC.core.call import SHUKLA
from SHUKLAMUSIC.utils import bot_sys_stats
from SHUKLAMUSIC.utils.decorators.language import language
from SHUKLAMUSIC.utils.inline import supp_markup
from config import BANNED_USERS


@app.on_message(filters.command("ping", prefixes=["/"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    start = datetime.now()
    # Changed from reply_video to reply
    response = await message.reply(
        text=_["ping_1"].format(app.mention),
    )
    pytgping = await SHUKLA.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_text(
        _["ping_2"].format(resp, app.mention, UP, RAM, CPU, DISK, pytgping),
        reply_markup=supp_markup(_),
    )