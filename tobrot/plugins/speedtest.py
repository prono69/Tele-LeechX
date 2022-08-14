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
┏━━━━━━━━━━━━━━━━━━╻
┣━━🚀 𝐒𝐩𝐞𝐞𝐝𝐭𝐞𝐬𝐭 𝐈𝐧𝐟𝐨:
┣ <b>Upload:</b> <code>{humanbytes(result['upload'] / 8)}/s</code>
┣ <b>Download:</b>  <code>{humanbytes(result['download'] / 8)}/s</code>
┣ <b>Ping:</b> <code>{result['ping']} ms</code>
┣ <b>Time:</b> <code>{result['timestamp']}</code>
┣ <b>Data Sent:</b> <code>{humanbytes(result['bytes_sent'])}</code>
┣ <b>Data Received:</b> <code>{humanbytes(result['bytes_received'])}</code>
┃
┣━━🌐 𝐒𝐩𝐞𝐞𝐝𝐭𝐞𝐬𝐭 𝐒𝐞𝐫𝐯𝐞𝐫:
┣ <b>Name:</b> <code>{result['server']['name']}</code>
┣ <b>Country:</b> <code>{result['server']['country']}, {result['server']['cc']}</code>
┣ <b>Sponsor:</b> <code>{result['server']['sponsor']}</code>
┣ <b>Latency:</b> <code>{result['server']['latency']}</code>
┣ <b>Latitude:</b> <code>{result['server']['lat']}</code>
┣ <b>Longitude:</b> <code>{result['server']['lon']}</code>
┃
┣━━👤 𝐂𝐥𝐢𝐞𝐧𝐭 𝐃𝐞𝐭𝐚𝐢𝐥𝐬:
┣ <b>IP Address:</b> <code>{result['client']['ip']}</code>
┣ <b>Latitude:</b> <code>{result['client']['lat']}</code>
┣ <b>Longitude:</b> <code>{result['client']['lon']}</code>
┣ <b>Country:</b> <code>{result['client']['country']}</code>
┣ <b>ISP:</b> <code>{result['client']['isp']}</code>
┣ <b>ISP Rating:</b> <code>{result['client']['isprating']}</code>
┃
┗━━━━━━━━━━━━━━━━━━╹
'''
    await imspd.delete()
    try:
        await message.reply_photo(path, caption=string_speed, parse_mode=enums.ParseMode.HTML)
    except:
        await message.reply(string_speed, parse_mode=enums.ParseMode.HTML)
    LOGGER.info(f'Server Speed result:-\nDL: {humanbytes(result["download"] / 8)}/s UL: {humanbytes(result["upload"] / 8)}/s')
