# This file is a part of TG-FileStreamBot

import asyncio,requests,base64,re
from WebStreamer.bot import StreamBot
from WebStreamer.utils.file_properties import gen_link
from WebStreamer.vars import Var
from pyrogram import filters, Client
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums.parse_mode import ParseMode

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
            updated_links = "\n".join([link_to_write])
            # updated_links = "\n".join(current_links + [link_to_write])
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
    # try:
        # check_member = await c.get_chat_member(-1002013292737, m.from_user.id)
    # except:
        
        # await m.reply("אין הרשאה")
        # return
    #chameleon 6712858787
    #apropo '613022086'
    # nokem 321416727
    # shani 7948678357
    # dikla '7578183815'
    # keren 5771387214
    # lital 7893340888
    # arik 7638774063
    # nofar 7038354195
    # ronen 973965945
    # yafit 7997603714
    # doron 5 7398789872
    # miki 6 7184535583
    # ofer 7 7539512427
    # miri 8 7828130943
    members=['384403734','1229060184','838481324','5667480303','5771387214','5984604232','5941680786','6022195851','6217448590','936713264','238358337','1686587448','226493193','613022086','321416727','7948678357','7578183815','5771387214','7893340888','7638774063','7038354195','973965945','7997603714','7398789872','7184535583','7539512427','7828130943']

    if str(m.from_user.id) not in members:
        await m.reply("😕")
        return
    try:
        # מעביר הודעה ולינק לערוץ משני
        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
        reply_markup, Stream_Text, stream_link = await gen_link(m=m, log_msg=log_msg, from_channel=False)
        send_link_to_github(Stream_Text)
        await log_msg.reply_text(text=f"**RᴇQᴜᴇꜱᴛᴇᴅ ʙʏ :** [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n**Uꜱᴇʀ ɪᴅ :** `{m.from_user.id}`\n**Dᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ :** {stream_link}", disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN, quote=True)
        # await asyncio.sleep(1.5)# ANONYMOUS
        # send_link_to_github(Stream_Text)
        # מעביר לינק הורדה לערוץ לינקים ישירים
        await c.send_message(chat_id=Var.LINK_HTTPS_CHANNEL, text=Stream_Text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True)
        
        # מחזיר לינק לבוט הראשי
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

@StreamBot.on_message(filters.channel & (filters.document | filters.video), group=-1)
async def channel_receive_handler(bot, broadcast: Message):
    # if int(broadcast.chat.id) in Var.BANNED_CHANNELS:
        # await bot.leave_chat(broadcast.chat.id)
        # return
    # if int(broadcast.chat.id) == int(Var.BIN_CHANNEL):
        # return
    try:
        log_msg = await broadcast.forward(chat_id=Var.BIN_CHANNEL)
        reply_markup, Stream_Text, stream_link = await gen_link(m=broadcast, log_msg=log_msg, from_channel=True)
        await log_msg.reply_text(
            text=f"**Cʜᴀɴɴᴇʟ Nᴀᴍᴇ:** `{broadcast.chat.title}`\n**Cʜᴀɴɴᴇʟ ID:** `{broadcast.chat.id}`\n**Rᴇǫᴜᴇsᴛ ᴜʀʟ:** {stream_link}",
            # text=f"**Cʜᴀɴɴᴇʟ Nᴀᴍᴇ:** `{broadcast.chat.title}`\n**Cʜᴀɴɴᴇʟ ID:** `{broadcast.chat.id}`\n**Rᴇǫᴜᴇsᴛ ᴜʀʟ:** https://t.me/FxStreamBot?start=msgid_{str(log_msg.id)}",
            quote=True,
            parse_mode=ParseMode.MARKDOWN
        )
        # await bot.edit_message_reply_markup(
            # chat_id=broadcast.chat.id,
            # message_id=broadcast.id,
            # reply_markup=InlineKeyboardMarkup(
                # [[InlineKeyboardButton("Dᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ 📥", url=stream_link)]])
        # )
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
        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
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

