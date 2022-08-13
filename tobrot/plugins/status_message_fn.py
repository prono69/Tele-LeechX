#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | 5MysterySD | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

import sys

from datetime import datetime
from math import floor
from asyncio import sleep as asleep, subprocess, create_subprocess_shell
from io import BytesIO, StringIO
from os import path as opath, remove as oremove
from shutil import disk_usage
from time import time, sleep as tsleep
from traceback import format_exc
from psutil import virtual_memory, cpu_percent, net_io_counters

from pyrogram.errors import FloodWait, MessageIdInvalid, MessageNotModified
from pyrogram import enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from tobrot.helper_funcs.admin_check import AdminCheck
from tobrot import (
    AUTH_CHANNEL,
    BOT_START_TIME,
    LOGGER,
    MAX_MESSAGE_LENGTH, 
    user_specific_config,
    gid_dict,
    _lock,
    EDIT_SLEEP_TIME_OUT,
    FINISHED_PROGRESS_STR,
    UN_FINISHED_PROGRESS_STR,
    UPDATES_CHANNEL,
    CANCEL_COMMAND_G,
    LOG_FILE_NAME,
    DB_URI,
    user_settings
    )
from tobrot.helper_funcs.display_progress import humanbytes, TimeFormatter
from tobrot.helper_funcs.download_aria_p_n import aria_start
from tobrot.helper_funcs.upload_to_tg import upload_to_tg
from tobrot.database.db_func import DatabaseManager
from tobrot.bot_theme.themes import BotTheme

async def upload_as_doc(client, message):
    uid = message.from_user.id
    user_specific_config[uid] = True
    if DB_URI:
        DatabaseManager().user_doc(uid)
        LOGGER.info("[DB] User Toggle DOC Settings Saved to Database")
    await message.reply_text(((BotTheme(uid)).TOGGLEDOC_MSG).format(
        u_men = message.from_user.mention,
        u_id = uid,
        UPDATES_CHANNEL = UPDATES_CHANNEL
    ))

async def upload_as_video(client, message):
    uid = message.from_user.id
    user_specific_config[uid] = False
    if DB_URI:
        DatabaseManager().user_vid(uid)
        LOGGER.info("[DB] User Toggle VID Settings Saved to Database")
    await message.reply_text(((BotTheme(uid)).TOGGLEVID_MSG).format(
        u_men = message.from_user.mention,
        u_id = uid,
        UPDATES_CHANNEL = UPDATES_CHANNEL
    ))

def progress_bar(percentage):
    p_used = '●'
    p_total = '○'
    if isinstance(percentage, str):
        return ''
    try:
        percentage=int(percentage)
    except:
        percentage = 0
    return ''.join(p_used if i <= percentage // 10 else p_total for i in range(10))

def bot_button_stats():
    hr, mi, se = up_time(time() - BOT_START_TIME)
    total, used, free = disk_usage(".")
    ram = virtual_memory().percent
    cpu = cpu_percent()
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    used_percent = (int(float(used[:-3])) / int(float(total[:-3]))) * 100
    sent = humanbytes(net_io_counters().bytes_sent)
    recv = humanbytes(net_io_counters().bytes_recv)
    return f'''
┏━━━━ 𝗕𝗼𝘁 𝗦𝘁𝗮𝘁𝘀 ━━━━━╻
┃ ᑕᑭᑌ: {progress_bar(cpu)} {cpu}% 
┃ ᖇᗩᗰ: {progress_bar(ram)} {ram}%  
┃ T-ᗪᒪ: {sent} ┃ T-ᑌᒪ: {recv}
┃ ᑌᑭ : {hr}h {mi}m {se}s
┃ T: {total} ┃ ᖴ: {free}
┃ ᗪIՏK: {progress_bar(used_percent)} {int(used_percent)}%
┗━━━━━━━━━━━━━━━━╹'''

async def status_message_f(client, message):
    aria_i_p = await aria_start()
    to_edit = await message.reply("🧭 𝐆𝐞𝐭𝐭𝐢𝐧𝐠 𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐒𝐭𝐚𝐭𝐮𝐬 . .")
    chat_id = int(message.chat.id)
    mess_id = int(to_edit.id)
    async with _lock:
        if len(gid_dict[chat_id]) == 0:
            gid_dict[chat_id].append(mess_id)
        elif mess_id not in gid_dict[chat_id]:
            await client.delete_messages(chat_id, gid_dict[chat_id])
            gid_dict[chat_id].pop()
            gid_dict[chat_id].append(mess_id)

    prev_mess = "FXTorrentz"
    await message.delete()
    while True:
        downloads = aria_i_p.get_downloads()
        msg = ""
        for file in downloads:
            downloading_dir_name = "N/A"
            try:
                downloading_dir_name = str(file.name)
            except:
                pass
            if file.status == "active":
                umess = user_settings[file.gid]
                percentage = int(file.progress_string(0).split('%')[0])
                prog = "[{0}{1}]".format(
                    "".join([FINISHED_PROGRESS_STR for _ in range(floor(percentage / 5))]),
                    "".join([UN_FINISHED_PROGRESS_STR for _ in range(20 - floor(percentage / 5))])
                )
                is_file = file.seeder
                curTime = time()
                msg += f"\n┏━━━━━━━━━━━━━━━━━━╻"
                msg += f"\n┣🗄 𝐍𝐚𝐦𝐞: <a href='{umess.link}'>{downloading_dir_name}</a>"
                msg += f"\n┣📈 𝐒𝐭𝐚𝐭𝐮𝐬: <i>Downloading...📥</i>"
                msg += f"\n┃<code>{prog}</code>"
                msg += f"\n┣⚡️ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐝: <code>{file.progress_string()}</code> <b>of</b> <code>{file.total_length_string()}</code>"
                msg += f"\n┣📡 𝐒𝐩𝐞𝐞𝐝: <code>{file.download_speed_string()}</code>,"
                msg += f"⏳️ 𝐄𝐓𝐀: <code>{file.eta_string()}</code>"
                try:
                    inTime = datetime.timestamp(datetime.strptime(str(umess.date),"%Y-%m-%d %H:%M:%S"))
                    msg += f"\n┣⏰️ 𝐄𝐥𝐚𝐬𝐩𝐞𝐝: <code>{TimeFormatter((curTime - inTime) * 1000)}</code>"
                except: pass
                msg += f"\n┣<b>👤 𝐔𝐬𝐞𝐫:</b> {umess.from_user.mention} ( #ID{umess.from_user.id} )"
                msg += f"\n┣<b>⚠️ 𝐖𝐚𝐫𝐧:</b> <code>/warn {umess.from_user.id}</code>"
                if is_file is None:
                    msg += f"\n┣📊 𝐂𝐨𝐧𝐧𝐞𝐜𝐭𝐢𝐨𝐧𝐬: <code>{file.connections}</code>"
                else:
                    msg += f"\n┣🍳𝐒𝐞𝐞𝐝𝐬: <code>{file.num_seeders}</code> ┃ 🔰𝐏𝐞𝐞𝐫𝐬: <code>{file.connections}</code>"
                msg += f"\n┣🚫 𝐓𝐨 𝐂𝐚𝐧𝐜𝐞𝐥: <code>/{CANCEL_COMMAND_G} {file.gid}</code>"
                msg += f"\n┗━━━━━━━━━━━━━━━━━━╹\n"

        ms_g = "◆━━━━━━━◆ ❃ ◆━━━━━━━◆"
        if UPDATES_CHANNEL:
            ms_g += f"\n♦️ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL}♦️"
        umen = f'<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>'
        mssg = f"\n❣𝙎𝙩𝙖𝙩𝙪𝙨 : {umen} (<code>{message.from_user.id}</code>)\n◆━━━━━━━◆ ❃ ◆━━━━━━━◆"

        button_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('Sᴛᴀᴛs\nCʜᴇᴄᴋ', callback_data="stats"),
             InlineKeyboardButton('Cʟᴏsᴇ', callback_data="admin_close")]
        ])

        if msg == "":
            msg = f"\n┏━━━━━━━━━━━━━━━━━━╻\n┃\n┃ ⚠️ <b>No Active, Queued or Paused \n┃ Torrents / Direct Links ⚠️</b>\n┃\n┗━━━━━━━━━━━━━━━━━━╹\n"
            msg = mssg + "\n" + msg + "\n" + ms_g
            await to_edit.edit(msg, reply_markup=button_markup)
            await asleep(EDIT_SLEEP_TIME_OUT)
            await to_edit.delete()
            break
        msg = mssg + "\n" + msg + "\n" + ms_g
        if len(msg) > MAX_MESSAGE_LENGTH:
            with BytesIO(str.encode(msg)) as out_file:
                out_file.name = "fxstatus.txt"
                await client.send_document(
                    chat_id=message.chat.id,
                    document=out_file,
                )
            break
        else:
            if msg != prev_mess:
                try:
                    await to_edit.edit(msg, parse_mode=enums.ParseMode.HTML, reply_markup=button_markup)
                except MessageIdInvalid:
                    break
                except MessageNotModified as ep:
                    LOGGER.info(ep)
                    await asleep(EDIT_SLEEP_TIME_OUT)
                except FloodWait as e:
                    LOGGER.info(f"FloodWait : Sleeping {e.value}s")
                    tsleep(e.value)
                await asleep(EDIT_SLEEP_TIME_OUT)
                prev_mess = msg


async def cancel_message_f(client, message):
    if len(message.command) > 1:
        i_m_s_e_g = await message.reply_text("<code>Checking..⁉️</code>", quote=True)
        aria_i_p = await aria_start()
        g_id = message.command[1].strip()
        LOGGER.info(g_id)
        try:
            downloads = aria_i_p.get_download(g_id)
            name = downloads.name
            size = downloads.total_length_string()
            gid_list = downloads.followed_by_ids
            downloads = [downloads]
            if len(gid_list) != 0:
                downloads = aria_i_p.get_downloads(gid_list)
            aria_i_p.remove(downloads=downloads, force=True, files=True, clean=True)
            await i_m_s_e_g.edit_text(f"⛔<b> Download Cancelled </b>⛔ :\n<code>{name} ({size})</code> By <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>")
        except Exception as e:
            await i_m_s_e_g.edit_text("<i>⚠️ FAILED ⚠️</i>\n\n" + str(e) + "\n#Error")
    else:
        await message.delete()

async def exec_message_f(client, message):
    DELAY_BETWEEN_EDITS = 0.3
    PROCESS_RUN_TIME = 100
    cmd = message.text.split(" ", maxsplit=1)[1]
    link = message.text.split(' ', maxsplit=1)[1]
    work_in = await message.reply_text("`Generating ...`")

    reply_to_id = message.id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.id

    start_time = time() + PROCESS_RUN_TIME
    process = await create_subprocess_shell(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e = stderr.decode()
    if not e:
        e = "No Error"
    o = stdout.decode()
    if not o:
        o = "No Output"
    else:
        _o = o.split("\n")
        o = "`\n".join(_o)
    OUTPUT = f"<b>QUERY:</b>\n\nCommand: {link} \n\nPID: <code>{process.pid}</code>\n\n<b>Stderr:</b> \n<code>{e}</code>\n<b>Output</b>:\n\n <code>{o}</code>"
    await work_in.delete()

    if len(OUTPUT) > MAX_MESSAGE_LENGTH:
        with BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "shell.txt"
            await client.send_document(
                chat_id=message.chat.id,
                document=out_file,
                caption=cmd,
                disable_notification=True,
                reply_to_message_id=reply_to_id,
            )
        await message.delete()
    else:
        await message.reply_text(OUTPUT, disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML, quote=True)

async def upload_document_f(client, message):
    imsegd = await message.reply_text("⚙️ Processing ...")
    if message.from_user.id in AUTH_CHANNEL and " " in message.text:
        recvd_command, local_file_name = message.text.split(" ", 1)
        recvd_response = await upload_to_tg(
            imsegd, local_file_name, message.from_user.id, {}, client
        )
        LOGGER.info(recvd_response)
    await imsegd.delete()

async def eval_message_f(client, message):
    if message.from_user.id not in AUTH_CHANNEL:
        return
    status_message = await message.reply_text("Processing ...")
    cmd = message.text.split(" ", maxsplit=1)[1]

    reply_to_id = message.id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.id

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = f"<b>EVAL</b>: <code>{cmd}</code>\n\n<b>OUTPUT</b>:\n<code>{evaluation.strip()}</code> \n"


    if len(final_output) > MAX_MESSAGE_LENGTH:
        with open("eval.text", "w+", encoding="utf8") as out_file:
            out_file.write(final_output)
        await message.reply_document(
            document="eval.text",
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=reply_to_id,
        )
        oremove("eval.text")
        await status_message.delete()
    else:
        await status_message.edit(final_output)


async def aexec(code, client, message):
    exec(
        (
            "async def __aexec(client, message): "
            + "".join(f"\n {l}" for l in code.split("\n"))
        )
    )

    return await locals()["__aexec"](client, message)


def up_time(time_taken):
    hours, _hour = divmod(time_taken, 3600)
    minutes, seconds = divmod(_hour, 60)
    return round(hours), round(minutes), round(seconds)


async def upload_log_file(client, message):
    ## No Kanged From Anywhere, Programmed By 5MysterySD >>>>>>>>
    logFile = await AdminCheck(client, message.chat.id, message.from_user.id)
    if logFile and opath.exists(LOG_FILE_NAME):
        logFileRead = open(LOG_FILE_NAME, "r")
        LOGGER.info("Generating LOG Display...")
        logFileLines = logFileRead.read().splitlines()
        toDisplay = 0
        toDisplay = min(len(logFileLines), 25)
        startLine = f'Last {toDisplay} Lines : [On Display Telegram LOG]\n\n---------------- START LOG -----------------\n\n'
        endLine = '\n---------------- END LOG -----------------'
        try:
            Loglines = ''.join(logFileLines[-l]+'\n\n' for l in range (toDisplay, 0, -1))
            Loglines = Loglines.replace('"', '')
            textLog = startLine+Loglines+endLine
            await message.reply_text(textLog,
                parse_mode=enums.ParseMode.DISABLED #tg Sucks
            )
        except Exception as err:
            LOGGER.info(f"Error Log Display : {err}")
            LOGGER.info(textLog)
        h, m, s = up_time(time() - BOT_START_TIME)
        await message.reply_document(LOG_FILE_NAME, caption=f"**Full Log**\n\n**Bot Uptime:** `{h}h, {m}m, {s}s`")

