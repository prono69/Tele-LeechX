#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | MaxxRider | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

import logging
import math
import time

from pyrogram.errors.exceptions import FloodWait
from tobrot import (
    EDIT_SLEEP_TIME_OUT,
    FINISHED_PROGRESS_STR,
    UN_FINISHED_PROGRESS_STR,
    gDict,
    LOGGER,
    UPDATES_CHANNEL 
)

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message



class Progress:
    def __init__(self, from_user, client, mess: Message):
        self._from_user = from_user
        self._client = client
        self._mess = mess
        self._cancelled = False

    @property
    def is_cancelled(self):
        chat_id = self._mess.chat.id
        mes_id = self._mess.id
        if gDict[chat_id] and mes_id in gDict[chat_id]:
            self._cancelled = True
        return self._cancelled

    async def progress_for_pyrogram(self, current, total, ud_type, start):
        chat_id = self._mess.chat.id
        mes_id = self._mess.id
        from_user = self._from_user
        now = time.time()
        diff = now - start
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⛔ 𝗖𝗔𝗡𝗖𝗘𝗟 ⛔",
                        callback_data=(
                            f"gUPcancel/{chat_id}/{mes_id}/{from_user}"
                        ).encode("UTF-8"),
                    )
                ]
            ]
        )
        if self.is_cancelled:
            LOGGER.info("stopping ")
            await self._mess.edit(
                f"⛔ **Cancelled / Error** ⛔ \n\n `{ud_type}` ({humanbytes(total)})"
            )
            await self._client.stop_transmission()

        if round(diff % float(EDIT_SLEEP_TIME_OUT)) == 0 or current == total:
            # if round(current / total * 100, 0) % 5 == 0:
            percentage = current * 100 / total
            speed = current / diff
            elapsed_time = round(diff) * 1000
            time_to_completion = round((total - current) / speed) * 1000
            estimated_total_time = time_to_completion

            elapsed_time = TimeFormatter(milliseconds=elapsed_time)
            estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

            progress = "┃\n┃<code>[{0}{1}] {2}%</code>\n┃\n".format(
                ''.join(
                    [
                        FINISHED_PROGRESS_STR
                        for _ in range(math.floor(percentage / 5))
                    ]
                ),
                ''.join(
                    [
                        UN_FINISHED_PROGRESS_STR
                        for _ in range(20 - math.floor(percentage / 5))
                    ]
                ),
                round(percentage, 2),
            )

            #cpu = "{psutil.cpu_percent()}%"
            tmp = progress + "┣⚡️ 𝐓𝐨𝐭𝐚𝐥 : `〚{1}〛`\n┣⚡️ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐝  :` 〚{0}〛`\n┣⚡️ 𝐒𝐩𝐞𝐞𝐝 : ` 〚{2}〛`\n┣⚡️ 𝐄𝐓𝐀 : `〚{3}〛`".format(
                humanbytes(current),
                humanbytes(total),
                humanbytes(speed),
                # elapsed_time if elapsed_time != '' else "0 s",
                estimated_total_time if estimated_total_time != "" else "0 s",
            )
            tmp += f"\n┗━♦️ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL}♦️━╹\n\n◆━━━━━━◆ ❃ ◆━━━━━━◆"
            try:
                if not self._mess.photo:
                    await self._mess.edit_text(
                        text=f"{ud_type}\n {tmp}", reply_markup=reply_markup
                    )

                else:
                    await self._mess.edit_caption(caption=f"{ud_type}\n {tmp}")
            except FloodWait as fd:
                LOGGER.warning(f"FloodWait : Sleeping {fd.value}s")
                time.sleep(fd.value)
            except Exception as ou:
                logger.info(ou)


def humanbytes(size) -> str:
    if not size:
        return ""
    power = 2 ** 10
    ind = 0
    SIZE_UNITS = {0: "", 1: "K", 2: "M", 3: "G", 4: "T", 5: "P", 6: "E", 7: "Z", 8: "Y"}
    while size > power:
        size /= power
        ind += 1
    try:
        return f"{str(round(size, 2))} {SIZE_UNITS[ind]}B"
    except IndexError:
        return 'File too large'

def humanbytes_int(size_str) -> str:
    size = int(size_str)
    if not size:
        return ""
    power = 2 ** 10
    ind = 0
    SIZE_UNITS = {0: "", 1: "K", 2: "M", 3: "G", 4: "T", 5: "P", 6: "E", 7: "Z", 8: "Y"}
    while size > power:
        size /= power
        ind += 1
    try:
        return f"{str(round(size, 2))} {SIZE_UNITS[ind]}B"
    except IndexError:
        return 'File too large'

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        (f"{int(days)}d, " if days else "")
        + (f"{int(hours)}h, " if hours else "")
        + (f"{int(minutes)}m, " if minutes else "")
        + (f"{int(seconds)}s, " if seconds else "")
        + (f"{int(milliseconds)}ms, " if milliseconds else "")
    )

    return tmp[:-2]
