import os
from pyrogram import filters
from MahakRobot import pbot as app
from pyrogram.errors import FloodWait


@app.on_edited_message(filters.group & ~filters.me)
async def delete_edited_messages(client, edited_message):
    try:
        await edited_message.delete()
    except FloodWait as e:
        await asyncio.sleep(e.x)


def time_formatter(milliseconds: float) -> str:
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"


def size_formatter(bytes: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            break
        bytes /= 1024.0
    return f"{bytes:.2f} {unit}"


def delete_long_messages(_, m):
    return len(m.text.split()) > 400 if m.text else False


@app.on_message(filters.group & delete_long_messages)
async def delete_and_reply(client, msg):
    try:
        await msg.delete()
        user_mention = msg.from_user.mention
        await app.send_message(msg.chat.id, f"✦ ʜᴇʏ {user_mention} ʙᴀʙʏ, ᴘʟᴇᴀsᴇ ᴋᴇᴇᴘ ʏᴏᴜʀ ᴍᴇssᴀɢᴇ sʜᴏʀᴛ.")
    except FloodWait as e:
        await asyncio.sleep(e.x)


@app.on_message(filters.group & filters.document)
async def message_handler(client, message):
    if message.document.mime_type == 'application/pdf':
        try:
            await message.delete()
        except FloodWait as e:
            await asyncio.sleep(e.x)