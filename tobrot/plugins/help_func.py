#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) 5MysterySD | Anasty17 [MLTB]
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

from os import path as opath
from time import time
from subprocess import check_output
from psutil import disk_usage, cpu_percent, swap_memory, cpu_count, virtual_memory, net_io_counters, boot_time
from pyrogram import enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tobrot import *
from tobrot.helper_funcs.display_progress import humanbytes, TimeFormatter
from tobrot.bot_theme.themes import BotTheme

async def stats(client, message):
    user_id = message.from_user.id
    stats = (BotTheme(user_id)).STATS_MSG_1
    if opath.exists('.git'):
        last_commit = check_output(["git log -1 --date=format:'%I:%M:%S %p %d %B, %Y' --pretty=format:'%cr ( %cd )'"], shell=True).decode()
    else:
        LOGGER.info("Stats : No UPSTREAM_REPO")
        last_commit = ''
    if last_commit:
        stats += ((BotTheme(user_id)).STATS_MSG_2).format(
        lc = last_commit
    )
    currentTime = TimeFormatter((time() - BOT_START_TIME)*1000)
    osUptime = TimeFormatter((time() - boot_time())*1000)
    total, used, free, disk= disk_usage('/')
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    sent = humanbytes(net_io_counters().bytes_sent)
    recv = humanbytes(net_io_counters().bytes_recv)
    cpuUsage = cpu_percent(interval=0.5)
    p_core = cpu_count(logical=False)
    t_core = cpu_count(logical=True)
    swap = swap_memory()
    swap_p = swap.percent
    swap_t = humanbytes(swap.total)
    memory = virtual_memory()
    mem_p = memory.percent
    mem_t = humanbytes(memory.total)
    mem_a = humanbytes(memory.available)
    mem_u = humanbytes(memory.used)
    stats += ((BotTheme(user_id)).STATS_MSG_3).format(
        ct = currentTime,
        osUp = osUptime,
        t = total,
        u = used,
        f = free,
        s = sent,
        r = recv,
        cpu = cpuUsage,
        mem = mem_p,
        di = disk,
        p_co = p_core,
        t_co = t_core,
        swap_t = swap_t,
        swap_p = swap_p,
        mem_t = mem_t,
        mem_a = mem_a,
        mem_u = mem_u,
        UPDATES_CHANNEL = UPDATES_CHANNEL
    )
    await message.reply_text(text = stats,
        parse_mode = enums.ParseMode.HTML,
        disable_web_page_preview=True
    )

async def help_message_f(client, message):

    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🆘️ Open Help 🆘️", callback_data = "openHelp_pg1")]]
    )
    await message.reply_text(
        text = ((BotTheme(message.from_user.id)).HELP_MSG).format(
        UPDATES_CHANNEL = UPDATES_CHANNEL
    ),
        reply_markup = reply_markup,
        parse_mode = enums.ParseMode.HTML,
        disable_web_page_preview=True
    )

async def user_settings(client, message):

    uid = message.from_user.id
    to_edit = await message.reply_text('Fetching your Details . . .')
    thumb_path = f'{DOWNLOAD_LOCATION}/thumbnails/{uid}.jpg'
    if not opath.exists(thumb_path):
        image = 'https://te.legra.ph/file/73712e784132c2af82731.jpg'
    else:
        image = thumb_path
    __theme = USER_THEMES.get(uid, 'Default Bot Theme')
    __prefix = PRE_DICT.get(uid, "-")
    __caption = CAP_DICT.get(uid, "-")
    __template = IMDB_TEMPLATE.get(uid, "Default Template")
    __toggle = user_specific_config.get(uid, False)
    toggle_ = 'Document' if __toggle else 'Video'
    __text = f'''┏━ 𝙐𝙨𝙚𝙧 𝘾𝙪𝙧𝙧𝙚𝙣𝙩 𝙎𝙚𝙩𝙩𝙞𝙣𝙜𝙨 ━━╻
┃
┣ <b>User Prefix :</b> <code>{__prefix}</code>
┣ <b>User Bot Theme :</b> <code>{__theme}</code>
┣ <b>User Caption :</b> <code>{__caption}</code>
┣ <b>User IMDB Template :</b> 
<code>{__template}</code>
┣ <b>User Toggle :</b> <code>{toggle_}</code>
┃
┗━━━━━━━━━━━━━━━━━━╹

'''
    await to_edit.delete()
    await message.reply_photo(photo = image, caption=__text, parse_mode=enums.ParseMode.HTML)
    
