#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) YashDK [TorToolKit] | 5MysterySD | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved


from speedtest import Speedtest
from pyrogram import enums

from tobrot import LOGGER
from tobrot.helper_funcs.display_progress import humanbytes

async def get_speed(self, message):
    imspd = await message.reply("`Running Speed Test...`")
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    path = (result['share'])
    string_speed = f'''
<code>🌐 Server :</code>
╠ <b>Name:</b> <code>{result['server']['name']}</code>
╠ <b>Country:</b> <code>{result['server']['country']}, {result['server']['cc']}</code>
╠ <b>Sponsor:</b> <code>{result['server']['sponsor']}</code>
╚ <b>ISP:</b> <code>{result['client']['isp']}</code>

<code>🧭 SpeedTest Results :</code>
╠ <b>Upload:</b> <code>{humanbytes(result['upload'] / 8)}</code>
╠ <b>Download:</b>  <code>{humanbytes(result['download'] / 8)}</code>
╠ <b>Ping:</b> <code>{result['ping']} ms</code>
╚ <b>ISP Rating:</b> <code>{result['client']['isprating']}</code>
'''
    await imspd.delete()
    try:
        await message.reply_photo(path, string_speed, parse_mode=enums.ParseMode.HTML)
    except:
        await message.reply(string_speed, parse_mode=enums.ParseMode.HTML)
    LOGGER.info(f'Server Speed result:-\nDL: {humanbytes(result["download"] / 8)}/s UL: {humanbytes(result["upload"] / 8)}/s')
