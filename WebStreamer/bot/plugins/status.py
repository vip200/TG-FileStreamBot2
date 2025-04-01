import time
import shutil
import psutil
import asyncio
from WebStreamer import StartTime
from WebStreamer.bot import StreamBot, work_loads
from pyrogram import filters, Client
from pyrogram.types import Message
from WebStreamer.utils.Translation import Language
from WebStreamer.utils.time_format import get_readable_time
from WebStreamer.utils.human_readable import humanbytes
from pyrogram.enums.parse_mode import ParseMode
from datetime import datetime, timedelta

# נשמור את נתוני התעבורה כשמתחיל הסקריפט
start_sent = psutil.net_io_counters().bytes_sent
start_recv = psutil.net_io_counters().bytes_recv

async def reset_traffic_data():
    global start_sent, start_recv
    while True:
        # חישוב הזמן הנותר עד 00:00
        now = datetime.now()
        midnight = datetime.combine(now.date(), datetime.min.time()) + timedelta(days=1)
        time_to_wait = (midnight - now).total_seconds()
        
        # המתנה עד שעה 00:00
        await asyncio.sleep(time_to_wait)
        
        # לאחר הגעת השעה 00:00, נאפס את המידע על תעבורת הרשת
        start_sent = psutil.net_io_counters().bytes_sent
        start_recv = psutil.net_io_counters().bytes_recv

        print("Network traffic data has been reset at midnight!")  # אפשר להוסיף הודעה כדי לבדוק אם זה קורה
def status_bot():
    
    total_connected = sum(work_loads.values())
    uptime = get_readable_time((time.time() - StartTime))
    total, used, free = shutil.disk_usage('.')

    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)

    # נתוני תעבורת הרשת הנוכחיים
    current_sent = psutil.net_io_counters().bytes_sent
    current_recv = psutil.net_io_counters().bytes_recv

    # חישוב ההפרש מאז שהסקריפט רץ
    sent = humanbytes(current_sent - start_sent)
    recv = humanbytes(current_recv - start_recv)

    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    
    sys_stat = f"""<b>Bot Uptime:</b> {uptime}
    <b>Total disk space:</b> {total}
    <b>Used:</b> {used}
    <b>Free:</b> {free}\n
    📊Data Usage📊\n<b>Upload:</b> {sent}
    <b>Down:</b> {recv}\n
    <b>CPU:</b> {cpuUsage}% 
    <b>RAM:</b> {memory}% 
    <b>Disk:</b> {disk}%\n
    <b>Total Connected Clients:</b> {total_connected}"""
    return sys_stat
@StreamBot.on_message(filters.command('status') & filters.private)
async def start(b: Client, m: Message):
    lang = Language(m)
    await m.reply_text(
        text=status_bot(),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )

# הפעלת פונקציית איפוס תעבורה ברקע
async def main():
    await asyncio.gather(reset_traffic_data())

# הפעלת הפונקציה הראשית
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
