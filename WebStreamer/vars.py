# This file is a part of TG-FileStreamBot

from os import environ
from dotenv import load_dotenv

load_dotenv()


class Var(object):
    MULTI_CLIENT = False
    API_ID = 22191690#int(environ.get("API_ID"))
    API_HASH = '52f7f2fd2a96132679eae22129f6f720'#str(environ.get("API_HASH"))
    BOT_TOKEN = '5010315993:AAG5RNiWdN4LepyTgP61DoReM89HoLyUCtg'#str(environ.get("BOT_TOKEN"))
    SLEEP_THRESHOLD = int(environ.get("SLEEP_THRESHOLD", "60"))  # 1 minte
    WORKERS = int(environ.get("WORKERS", "6"))  # 6 workers = 6 commands at once
    BIN_CHANNEL = -1001689905120#int(
      #  environ.get("BIN_CHANNEL", None)
    #)  # you NEED to use a CHANNEL when you're using MULTI_CLIENT
    PORT = int(environ.get("PORT", 8080))
    BIND_ADDRESS = str(environ.get("WEB_SERVER_BIND_ADDRESS", "0.0.0.0"))
    PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))  # 20 minutes
    HAS_SSL = environ.get("HAS_SSL", False)
    HAS_SSL = True if str(HAS_SSL).lower() == "true" else False
    NO_PORT = environ.get("NO_PORT", False)
    NO_PORT = True if str(NO_PORT).lower() == "true" else False
    # if "DYNO" in environ:
    ON_HEROKU = True
    APP_NAME = 'rrr333-6d3a84e4ba29'#str(environ.get("APP_NAME"))
    # else:
        # ON_HEROKU = False
    FQDN = (
        str(environ.get("FQDN", BIND_ADDRESS))
        if not ON_HEROKU or environ.get("FQDN")
        else APP_NAME + ".herokuapp.com"
    )
    if ON_HEROKU:
        URL = f"https://{FQDN}/"
    else:
        URL = "http{}://{}{}/".format(
            "s" if HAS_SSL else "", FQDN, "" if NO_PORT else ":" + str(PORT)
        )

    UPDATES_CHANNEL = '-1001689905120'#str(environ.get('UPDATES_CHANNEL', "aredirect"))
    OWNER_ID = 384403734#int(environ.get('OWNER_ID', '777000'))

    BANNED_CHANNELS = -1001689905120#list(set(int(x) for x in str(environ.get("BANNED_CHANNELS", "-1001296894100")).split()))