#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 |5MysterySD | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

from asyncio import sleep as asleep
from os import path as opath, makedirs as omakedirs
from time import time
from pathlib import Path

from tobrot import DOWNLOAD_LOCATION, LOGGER, TELEGRAM_LEECH_UNZIP_COMMAND
from tobrot.helper_funcs.create_compressed_archive import unzip_me, get_base_name
from tobrot.helper_funcs.display_progress import Progress, TimeFormatter, humanbytes
from tobrot.helper_funcs.upload_to_tg import upload_to_gdrive
from tobrot.bot_theme.themes import BotTheme

async def down_load_media_f(client, message):  # to be removed
    user_command = message.command[0]
    user_id = message.from_user.id

    if message.reply_to_message is not None:
        the_real_download_location, mess_age = await download_tg(client, message)
        the_real_download_location_g = the_real_download_location
        if user_command == TELEGRAM_LEECH_UNZIP_COMMAND.lower():
            try:
                check_ifi_file = get_base_name(the_real_download_location)
                file_up = await unzip_me(the_real_download_location)
                if opath.exists(check_ifi_file):
                    the_real_download_location_g = file_up
            except Exception as ge:
                LOGGER.info(ge)
                LOGGER.info(
                    f"Can't extract {opath.basename(the_real_download_location)}, Uploading the same file"
                )
        await upload_to_gdrive(the_real_download_location_g, mess_age, message, user_id)
    else:
        await mess_age.edit_text(
            "Reply to a Telegram Media, to upload to the Cloud Drive."
        )

async def download_tg(client, message):

    user_id = message.from_user.id
    mess_age = await message.reply_text((BotTheme(user_id)).START_DOWM_MSG, quote=True)
    if not opath.isdir(DOWNLOAD_LOCATION):
        omakedirs(DOWNLOAD_LOCATION)
    rep_mess = message.reply_to_message
    if rep_mess is not None:
        file = [rep_mess.document, rep_mess.video, rep_mess.audio]
        file_name = [fi for fi in file if fi is not None][0].file_name
        start_t = time()
        download_location = str(Path("./").resolve()) + "/"
        c_time = time()
        prog = Progress(user_id, client, mess_age)
        try:
            the_real_download_location = await client.download_media(
                message=message.reply_to_message,
                file_name=download_location,
                progress=prog.progress_for_pyrogram,
                progress_args=(((BotTheme(user_id)).TOP_PROG_MSG).format(base_file_name = file_name), 
                    c_time
                )
            )
        except Exception as g_e:
            await mess_age.edit(f"⛔️ Error : {g_e}")
            LOGGER.error(g_e)
            return
        end_t = time()
        ms = (end_t - start_t)
        LOGGER.info(the_real_download_location)
        await asleep(2)
        if the_real_download_location:
            try:
                await mess_age.edit_text(((BotTheme(user_id)).DOWN_RE_COM_MSG).format(
                    base_file_name = opath.basename(the_real_download_location),
                    file_size = humanbytes(opath.getsize(the_real_download_location)),
                    tt = TimeFormatter(ms * 1000)
                ))
            except MessageNotModified:
                pass
        else:
            await mess_age.edit_text("<b>⛔ Download Cancelled ⛔\n\n User Cancelled or Telegram Download Error or Server Issue, Try Again ⁉️</b>")
            return None, mess_age
    return the_real_download_location, mess_age
