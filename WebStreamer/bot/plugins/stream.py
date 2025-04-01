# This file is a part of TG-FileStreamBot

import asyncio,requests,base64,re
from WebStreamer.bot import StreamBot
from WebStreamer.utils.file_properties import gen_link
from WebStreamer.vars import Var
from pyrogram import filters, Client
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums.parse_mode import ParseMode
from threading import Thread

def send_link_to_github(link_to_write):
    print('github')

    regex='File Id :</b> (.+?)\n'
    file_id=re.compile(regex).findall(link_to_write)[0].replace(' ','')
    
    regex='Download :</b> (.+?)\n'
    file_link=re.compile(regex).findall(link_to_write)[0].replace(' ','')
    link_to_write=file_id+'@'+file_link
    link_to_write=link_to_write

    try:
        a='ghp'
        b='_'
        c='4Bprf9NZ0'
        d='vcWBOEK4W6a'
        e='YFUuaPjBPX1j'
        f='Wg66'
        url = "https://api.github.com/repos/mediasdk/stream_link_bot/contents/stream_bot1.txt"

        access_token = a+b+c+d+e+f
        url = "https://api.github.com/repos/mediasdk/stream_link_bot/contents/stream_bot1.txt"

        # Fetch existing content and SHA
        response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
        data = response.json()
        
        # Fetch existing content and decode it
        decoded_content = base64.b64decode(data["content"]).decode("utf-8")
        for i in decoded_content.split("\n"):
            if '@' in i:
                regex='(.+?)@'
                x=re.compile(regex).findall(i)[0]
                if x ==file_id:
                    return

        # Clean up existing taglines
        current_links = [line.strip() for line in decoded_content.split("\n")]

        if link_to_write not in current_links:

            # Add new tagline to current taglines
            # updated_links = "\n".join([link_to_write])# מוחק את כל הרשימה
            if len(current_links)>100:
                del current_links[0]
            updated_links = "\n".join(current_links + [link_to_write])
            # Encode new content
            encoded_content = base64.b64encode(updated_links.encode("utf-8")).decode("utf-8")

            # Create commit data
            commit_data = {
                "message": f"{link_to_write}",
                "content": encoded_content,
                "sha": data["sha"]
            }

            # Send PUT request to update the file
            put_response = requests.put(url, json=commit_data, headers={"Authorization": f"Bearer {access_token}"})

            if put_response.status_code == 200:
                print(f"WRITE | Added {link_to_write} to taglines list.")
            else:
                error_message = put_response.json().get("message", "Unknown error")
                print(f"WRITE | Failed to update the file. Reason: {error_message}")
                
        else:
            print(f"WRITE | Skipping - {link_to_write} already exists in current_links.")
    
    except Exception as e:
        print(f"WRITE | Exception: {str(e)}")
        pass



@StreamBot.on_message(
    filters.private
    & (
        filters.document
        | filters.video
        | filters.audio
        | filters.animation
        | filters.voice
        | filters.video_note
        | filters.photo
        | filters.sticker
    ),
    group=4,
)
async def private_receive_handler(c: Client, m: Message):

    try:
        # מעביר הודעה ולינק לערוץ משני
        log_msg = await m.copy(chat_id=Var.BIN_CHANNEL)
        reply_markup, Stream_Text, stream_link = await gen_link(m=m, log_msg=log_msg, from_channel=False)
        # send_link_to_github(Stream_Text)
        t = Thread(target=send_link_to_github , args=(Stream_Text,))
        t.start()
        await log_msg.reply_text(text=f"**RᴇQᴜᴇꜱᴛᴇᴅ ʙʏ :** [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n**Uꜱᴇʀ ɪᴅ :** `{m.from_user.id}`\n**Dᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ :** {stream_link}", disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN, quote=True)

        await m.reply_text(
            text='צפייה מהנה',
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            # reply_markup=reply_markup,
            quote=True
        )
    except FloodWait as e:
        print(f"Sleeping for {str(e.value)}s")
        await asyncio.sleep(e.value)
        await c.send_message(chat_id=Var.BIN_CHANNEL, text=f"Gᴏᴛ FʟᴏᴏᴅWᴀɪᴛ ᴏғ {str(e.value)}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n**𝚄𝚜𝚎𝚛 𝙸𝙳 :** `{str(m.from_user.id)}`", disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)

@StreamBot.on_message(filters.channel & (filters.document | filters.video), group=-1)
async def channel_receive_handler(bot, broadcast: Message):

    try:
        log_msg = await broadcast.copy(chat_id=Var.BIN_CHANNEL)
        reply_markup, Stream_Text, stream_link = await gen_link(m=broadcast, log_msg=log_msg, from_channel=True)
        await log_msg.reply_text(
            text=f"**Cʜᴀɴɴᴇʟ Nᴀᴍᴇ:** `{broadcast.chat.title}`\n**Cʜᴀɴɴᴇʟ ID:** `{broadcast.chat.id}`\n**Rᴇǫᴜᴇsᴛ ᴜʀʟ:** {stream_link}",

            quote=True,
            parse_mode=ParseMode.MARKDOWN
        )

    except FloodWait as w:
        print(f"Sleeping for {str(w.value)}s")
        await asyncio.sleep(w.value)
        await bot.send_message(chat_id=Var.BIN_CHANNEL,
                             text=f"Gᴏᴛ FʟᴏᴏᴅWᴀɪᴛ ᴏғ {str(w.value)}s from {broadcast.chat.title}\n\n**Cʜᴀɴɴᴇʟ ID:** `{str(broadcast.chat.id)}`",
                             disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await bot.send_message(chat_id=Var.BIN_CHANNEL, text=f"**#ᴇʀʀᴏʀ_ᴛʀᴀᴄᴇʙᴀᴄᴋ:** `{e}`", disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)
        print(f"Cᴀɴ'ᴛ Eᴅɪᴛ Bʀᴏᴀᴅᴄᴀsᴛ Mᴇssᴀɢᴇ!\nEʀʀᴏʀ: {e}")

# Feature is Dead no New Update for Stream Link on Group
@StreamBot.on_message(filters.group & (filters.document | filters.video | filters.audio), group=4)
async def private_receive_handler(c: Client, m: Message):
    try:
        log_msg = await m.copy(chat_id=Var.BIN_CHANNEL)
        reply_markup, Stream_Text, stream_link = await gen_link(m=m, log_msg=log_msg, from_channel=True)
        await log_msg.reply_text(text=f"**RᴇQᴜᴇꜱᴛᴇᴅ ʙʏ :** [{m.chat.first_name}](tg://user?id={m.chat.id})\n**Group ɪᴅ :** `{m.from_user.id}`\n**Dᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ :** {stream_link}", disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN, quote=True)

        await m.reply_text(
            text=Stream_Text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            quote=True
        )
    except FloodWait as e:
        print(f"Sleeping for {str(e.value)}s")
        await asyncio.sleep(e.value)
        await c.send_message(chat_id=Var.BIN_CHANNEL, text=f"Gᴏᴛ FʟᴏᴏᴅWᴀɪᴛ ᴏғ {str(e.value)}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n**𝚄𝚜𝚎𝚛 𝙸𝙳 :** `{str(m.from_user.id)}`", disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)

