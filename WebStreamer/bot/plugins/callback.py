# This file is a part of TG-FileStreamBot

import random
from WebStreamer.bot import StreamBot
from WebStreamer.utils.file_properties import gen_link, get_media_file_unique_id
from WebStreamer.vars import Var
from WebStreamer.utils.Translation import Language, BUTTON
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import MessageDeleteForbidden
from pyrogram.enums.parse_mode import ParseMode
from WebStreamer.bot.plugins.status import status_bot
MY_USER_ID = 384403734
deldbtnmsg=["Your Already Deleted the Link", "You can't undo the Action", "You can Resend the File to Regenerate New Link", "Why Clicking me Your Link is Dead", "This is Just a Button Showing that Your Link is Deleted"]

import subprocess

async def test_speed(update):
    # הרצת speedtest-cli בתהליך עם פלט בזמן אמת
    process = subprocess.Popen(['speedtest-cli', '--secure'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # יצירת הודעה ראשונית למשתמש
    msg = await update.message.reply_text("בודק מהירות... אנא המתן...") 

    # קריאה לפלט בזמן אמת
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())  # הצגת הפלט בזמן אמת
            # שליחת הודעה חדשה עם פלט הבדיקה
            await update.message.reply_text(output.strip())  # שליחת הודעה חדשה

    # אם יש שגיאות
    error = process.stderr.read()
    if error:
        await update.message.reply_text(f"שגיאה בבדיקת המהירות: {error.strip()}")  # שליחת הודעה חדשה עם השגיאה
        print(f"שגיאה בבדיקת המהירות: {error.strip()}")
    await update.message.reply_text("בדיקת המהירות הסתיימה!",
        reply_markup=BUTTON.START_BUTTONS)



@StreamBot.on_callback_query()
async def cb_data(bot, update: CallbackQuery):
    if update.from_user.id != MY_USER_ID:
        await update.answer("הכפתור הזה מיועד רק למפתח!", show_alert=True)
        return  # אם המשתמש לא אתה, תפסיק את הפעולה
    lang = Language(update)
    if update.data == "home":
        await update.message.edit_text(
            text=lang.START_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=BUTTON.START_BUTTONS
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=lang.HELP_TEXT.format(Var.UPDATES_CHANNEL),
            disable_web_page_preview=True,
            reply_markup=BUTTON.HELP_BUTTONS
        )
    elif update.data == "status":
        await update.message.edit_text(
            text=status_bot(),
            disable_web_page_preview=True,
            reply_markup=BUTTON.START_BUTTONS
        )
    elif update.data == "speed_test":
        await test_speed(update) 
        await update.message.edit_text(
            text="בדיקת מהירות מתבצעת...",
            disable_web_page_preview=True,
            reply_markup=BUTTON.START_BUTTONS
        )
            
    elif update.data == "close":
        await update.message.delete()
    elif update.data == "msgdeleted":
        await update.answer(random.choice(deldbtnmsg), show_alert=True)
    else:
        usr_cmd = update.data.split("_")
        if usr_cmd[0] == "msgdelconf2":
            await update.message.edit_text(
            text=update.message.text,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✔️", callback_data=f"msgdelyes_{usr_cmd[1]}_{usr_cmd[2]}"), InlineKeyboardButton("✖️", callback_data=f"msgdelno_{usr_cmd[1]}_{usr_cmd[2]}")]])
        )
        elif usr_cmd[0] == "msgdelno":
            get_msg = await bot.get_messages(chat_id=Var.BIN_CHANNEL, message_ids=int(usr_cmd[1]))
            if get_media_file_unique_id(get_msg) == usr_cmd[2]:
                reply_markup, Stream_Text, stream_link = await gen_link(m=update, log_msg=get_msg, from_channel=False)
                # await asyncio.sleep(10)# ANONYMOUS
                await update.message.edit_text(
                text=Stream_Text,
                disable_web_page_preview=True,
                reply_markup=reply_markup
                )
            elif resp.empty:
                await update.answer("Sorry Your File is Missing from the Server", show_alert=True)
            else:
                await update.answer("Message id and file_unique_id miss match", show_alert=True)
        elif usr_cmd[0] == "msgdelyes":
            try:
                resp = await bot.get_messages(Var.BIN_CHANNEL, int(usr_cmd[1]))
                if get_media_file_unique_id(resp) == usr_cmd[2]:
                    await bot.delete_messages(
                        chat_id=Var.BIN_CHANNEL,
                        message_ids=int(usr_cmd[1])
                    )
                    await update.message.edit_text(
                    text=update.message.text,
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Link Deleted", callback_data="msgdeleted")]])
                    )
                elif resp.empty:
                    await update.answer("Sorry Your File is Missing from the Server", show_alert=True)
                else:
                    await update.answer("Message id and file_unique_id miss match", show_alert=True)
            except MessageDeleteForbidden as e:
                print(e)
                await bot.send_message(
                    chat_id=Var.BIN_CHANNEL,
                    text=f"**#ᴇʀʀᴏʀ_ᴛʀᴀᴄᴇʙᴀᴄᴋ:** `{e}`\n#Delete_Link", disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN,
                )
                await update.answer(text='message too old', show_alert=True)
            except Exception as e:
                print(e)
                error_id=await bot.send_message(
                    chat_id=Var.BIN_CHANNEL,
                    text=f"**#ᴇʀʀᴏʀ_ᴛʀᴀᴄᴇʙᴀᴄᴋ:** `{e}`\n#Delete_Link", disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN,
                )
                await update.message.reply_text(
                    text=f"**#ᴇʀʀᴏʀ_ᴛʀᴀᴄᴇʙᴀᴄᴋ:** `message-id={error_id.message_id}`\nYou can get Help from [Public Link Generator (Support)](https://t.me/{Var.UPDATES_CHANNEL})", disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN,
                )
        else:
            await update.message.delete()
