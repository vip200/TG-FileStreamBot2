# This file is a part of TG-FileStreamBot
import os
from os import environ
from dotenv import load_dotenv

load_dotenv()

class Var(object):
    MULTI_CLIENT = True
    API_ID = 22191690
    API_HASH = '52f7f2fd2a96132679eae22129f6f720'
    BOT_TOKEN = '5007581156:AAErP_wPdQGrHe101h4yKLD360rbLWyq5Vo'
    UPDATES_CHANNEL = '-1001689905120'
    OWNER_ID = 384403734
    SLEEP_THRESHOLD = int(environ.get("SLEEP_THRESHOLD", "60"))  # 1 minte
    WORKERS = int(environ.get("WORKERS", "6"))  # 6 workers = 6 commands at once
    BIN_CHANNEL = -1001689905120
    PORT = int(environ.get("PORT", 8080))
    BIND_ADDRESS = str(environ.get("WEB_SERVER_BIND_ADDRESS", "0.0.0.0"))
    PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))  # 20 minutes
    HAS_SSL = True
    NO_PORT = True
    FQDN = 'rrr333-6d3a84e4ba29.heroku.com'
    URL = "http{}://{}{}/".format(
        "s" if HAS_SSL else "", FQDN, "" if NO_PORT else ":" + str(PORT)
    )

    # MULTI_TOKEN1=7721797701:AAFrCfa-Tb223s8v-6gWR7BphMJGW3TaSuI @filestreamaxbot
    #MULTI_TOKEN2=7608239579:AAE5WLIsdtaN_uZYF-BOxZ_FDhJRkppqbNE  @filestreamax2bot
    #MULTI_TOKEN3=7677925864:AAFhCfw0cWGvTE1ioL8lgYP4lRO5SLkVSuI  @filestreamax3bot
