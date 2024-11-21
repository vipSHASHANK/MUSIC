import asyncio
import importlib
import threading
from flask import Flask
import requests
import time

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from SHUKLAMUSIC import LOGGER, app, userbot
from SHUKLAMUSIC.core.call import SHUKLA
from SHUKLAMUSIC.misc import sudo
from SHUKLAMUSIC.plugins import ALL_MODULES
from SHUKLAMUSIC.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

# Flask app initialize kar rahe hain
flask_app = Flask(__name__)

# Flask app ka ek basic route
@flask_app.route('/')
def home():
    return "Flask app running on port 80"

# Flask app ko alag thread mein run karne ka function
def run_flask():
    flask_app.run(host="0.0.0.0", port=80)

# Keep-alive function jo regular ping bhejta rahega
def keep_alive():
    while True:
        try:
            # Apne Render app ka URL daal kar ping karein
            requests.get("https://web-l2xjgmc8wvg8.up-de-fra1-k8s-1.apps.run-on-seenode.com/")
        except Exception as e:
            print(f"Ping error: {e}")
        # Har 5 minute mein ping karein
        time.sleep(300)

async def init():
    if not config.STRING1:
        LOGGER(__name__).error("𝐒𝐭𝐫𝐢𝐧𝐠 𝐒𝐞𝐬𝐬𝐢𝐨𝐧 𝐍𝐨𝐭 𝐅𝐢𝐥𝐥𝐞𝐝, 𝐏𝐥𝐞𝐚𝐬𝐞 𝐅𝐢𝐥𝐥 𝐀 𝐏𝐲𝐫𝐨𝐠𝐫𝐚𝐦 𝐒𝐞𝐬𝐬𝐢𝐨𝐧")
        exit()

    await sudo()
    try:
        # Get banned users and add them to the BANNED_USERS list
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass

    await app.start()

    # Import all plugins dynamically
    for all_module in ALL_MODULES:
        importlib.import_module("SHUKLAMUSIC.plugins" + all_module)
    
    LOGGER("SHUKLAMUSIC.plugins").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 𝐁𝐚𝐛𝐲🥳...")

    # Start userbot and SHUKLA
    await userbot.start()
    await SHUKLA.start()

    try:
        # Start streaming a media file
        await SHUKLA.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("SHUKLAMUSIC").error("𝗣𝗹𝗭 𝗦𝗧𝗔𝗥𝗧 𝗬𝗢𝗨𝗥 𝗟𝗢𝗚 𝗚𝗥𝗢𝗨𝗣 𝗩𝗢𝗜𝗖𝗘𝗖𝗛𝗔𝗧\𝗖𝗛𝗔𝗡𝗡𝗘𝗟\n\n𝗦𝗛𝗨𝗞𝗟𝗔𝗠𝗨𝗦𝗜𝗖 𝗕𝗢𝗧 𝗦𝗧𝗢𝗣........")
        exit()
    except:
        pass

    await SHUKLA.decorators()

    LOGGER("SHUKLAMUSIC").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎𝗠𝗔𝗗𝗘 𝗕𝗬 𝗠𝗥 𝗦𝗛𝗔𝗦𝗛𝗔𝗡𝗞\n╚═════ஜ۩۞۩ஜ════╝"
    )

    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("SHUKLAMUSIC").info("𝗦𝗧𝗢𝗣 𝗦𝗛𝗨𝗞𝗟𝗔 𝗠𝗨𝗦𝗜𝗖🎻 𝗕𝗢𝗧..")

if __name__ == "__main__":
    # Start Flask and keep-alive in separate threads
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True  # Ensure the Flask thread stops when the main program exits
    flask_thread.start()

    keep_alive_thread = threading.Thread(target=keep_alive)
    keep_alive_thread.daemon = True  # Ensure the keep-alive thread stops when the main program exits
    keep_alive_thread.start()

    # Run the bot asynchronously
    asyncio.get_event_loop().run_until_complete(init())