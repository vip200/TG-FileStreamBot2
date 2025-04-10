# This file is a part of TG-FileStreamBot

import sys,json,codecs
import asyncio
import logging,time
from .vars import Var
from aiohttp import web
from pyrogram import idle
from WebStreamer import utils
from WebStreamer import StreamBot
from WebStreamer.server import web_server
from WebStreamer.bot.clients import initialize_clients
from pyrogram.errors import FloodWait


logging.basicConfig(
    level=logging.INFO,
    datefmt="%d/%m/%Y %H:%M:%S",
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(stream=sys.stdout),
              logging.FileHandler("streambot.log", mode="a", encoding="utf-8")],)

logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

server = web.AppRunner(web_server())

#if sys.version_info[1] > 9:
#    loop = asyncio.new_event_loop()
#    asyncio.set_event_loop(loop)
#else:
loop = asyncio.get_event_loop()

async def send_startup_message():
    try:
        channel_id = Var.BIN_CHANNEL  # ה-ID של הערוץ שלך
        message_text = "✅ הבוט הופעל בהצלחה!"
        await StreamBot.send_message(channel_id, message_text)
        logging.info("הודעת הפעלה נשלחה לערוץ בהצלחה.")
    except Exception as e:
        logging.error(f"שגיאה בשליחת ההודעה לערוץ: {e}")



async def start_services():
    print()
    print("-------------------- Initializing Telegram Bot --------------------")
    await StreamBot.start()
    bot_info = await StreamBot.get_me()
    StreamBot.username = bot_info.username
    print("------------------------------ DONE ------------------------------")
    print()
    print(
        "---------------------- Initializing Clients ----------------------"
    )
    await initialize_clients()
    print("------------------------------ DONE ------------------------------")
    print("--------------------- Initalizing Web Server ---------------------")
    await server.setup()
    bind_address = Var.BIND_ADDRESS
    await web.TCPSite(server, bind_address, Var.PORT).start()
    print("------------------------------ DONE ------------------------------")
    print()
    print("------------------------- Service Started -------------------------")
    print("                        bot =>> {}".format(bot_info.first_name))
    if bot_info.dc_id:
        print("                        DC ID =>> {}".format(str(bot_info.dc_id)))
    print("                        server ip =>> {}".format(bind_address, Var.PORT))

    print("------------------------------------------------------------------")
    await send_startup_message()
    await idle()

async def cleanup():
    await server.cleanup()
    await StreamBot.stop()

if __name__ == "__main__":
    
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        pass

    except FloodWait as e:
        print(e.value)
        time.sleep(e.value)  # Wait "value" seconds before continuing
        loop.run_until_complete(start_services())
        
    except Exception as err:
        logging.error(err.with_traceback(None))
    
    finally:

        loop.run_until_complete(cleanup())
        loop.stop()
        print("------------------------ Stopped Services ------------------------")
