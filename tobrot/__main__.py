#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | MaxxRider | 5MysterySD | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

import logging
import os
import shutil
import datetime
import requests
import heroku3

from telegram import ParseMode
from pyrogram import enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import filters, idle
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from sys import executable
from subprocess import run as srun

from tobrot import HEROKU_API_KEY, HEROKU_APP_NAME, app, bot, __version__
from tobrot import (
    OWNER_ID,
    SUDO_USERS,
    AUTH_CHANNEL,
    DOWNLOAD_LOCATION,
    GET_SIZE_G,
    GLEECH_COMMAND,
    GLEECH_UNZIP_COMMAND,
    GLEECH_ZIP_COMMAND,
    LOGGER,
    RENEWME_COMMAND,
    TELEGRAM_LEECH_UNZIP_COMMAND,
    TELEGRAM_LEECH_COMMAND,
    UPLOAD_COMMAND,
    GYTDL_COMMAND,
    GPYTDL_COMMAND,
    RCLONE_COMMAND,
    UPDATES_CHANNEL,
    SERVER_HOST,
    LEECH_LOG,
    STRING_SESSION,
    SET_BOT_COMMANDS,
    RDM_QUOTE,
    INDEX_SCRAPE
)
if STRING_SESSION:
    from tobrot import userBot
from tobrot.helper_funcs.download import down_load_media_f
from tobrot.helper_funcs.download_aria_p_n import aria_start
from tobrot.plugins import *
from tobrot.plugins.index_scrape import index_scrape
from tobrot.plugins.call_back_button_handler import button
from tobrot.plugins.imdb import imdb_search
from tobrot.plugins.torrent_search import searchhelp
from tobrot.plugins.custom_utils import prefix_set, caption_set, template_set, theme_set
from tobrot.plugins.url_parser import url_parser
from tobrot.helper_funcs.bot_commands import BotCommands
from tobrot.database.db_func import DatabaseManager
from tobrot.plugins.choose_rclone_config import rclone_command_f
from tobrot.plugins.custom_thumbnail import clear_thumb_nail, save_thumb_nail
from tobrot.plugins.incoming_message_fn import (g_clonee, g_yt_playlist,
                                                incoming_message_f,
                                                incoming_purge_message_f,
                                                incoming_youtube_dl_f,
                                                rename_tg_file)
from tobrot.plugins.help_func import help_message_f, stats, user_settings
from tobrot.plugins.speedtest import get_speed
from tobrot.plugins.mediainfo import mediainfo
from tobrot.plugins.rclone_size import check_size_g, g_clearme
from tobrot.plugins.status_message_fn import (
    cancel_message_f,
    eval_message_f,
    exec_message_f,
    status_message_f,
    upload_document_f,
    upload_log_file,
    upload_as_doc,
    upload_as_video
)

if SET_BOT_COMMANDS:
    botcmds = [
        (f'{BotCommands.LeechCommand}', '📨 [Reply] Leech any Torrent/ Magnet/ Direct Link '),
        (f'{BotCommands.ExtractCommand}', '🔐 Unarchive items . .'),
        (f'{BotCommands.ArchiveCommand}', '🗜 Archive as .tar.gz acrhive... '),
        (f'{BotCommands.ToggleDocCommand}', '📂 Toggle to Document Upload '),
        (f'{BotCommands.ToggleVidCommand}', '🎞 Toggle to Streamable Upload '),
        (f'{BotCommands.SaveCommand}', '🖼 Save Thumbnail For Uploads'),
        (f'{BotCommands.ClearCommand}', '🕹 Clear Thumbnail '),
        (f'{BotCommands.RenameCommand}', '📧 [Reply] Rename Telegram File '),
        (f'{BotCommands.StatusCommand}', '🖲 Show Bot stats and concurrent Downloads'),
        (f'{BotCommands.SpeedCommand}', '📡 Get Current Server Speed of Your Bot'),
        (f'{BotCommands.YtdlCommand}', '🧲 [Reply] YT-DL Links for Uploading...'),
        (f'{BotCommands.PytdlCommand}', '🧧 [Reply] YT-DL Playlists Links for Uploading...'),
        (f'{BotCommands.GCloneCommand}', '♻️ [G-Drive] Clone Different Supported Sites !!'),
        (f'{BotCommands.StatsCommand}', '📊 Show Bot Internal Statistics'),
        (f'{BotCommands.MediaInfoCommand}', '🆔️ [Reply] Get Telegram Files Media Info'),
        ('setpre', '🔠 <Text> Save Custom Prefix for Uploads'),
        ('setcap', '🔣 <Text> Save Custom Caption for Uploads'),
        ('parser', '🧮 <URL> Get Bypassed Link After Parsing !!'),
        ('imdb', '🎬 [Title] Get IMDb Details About It !!'),
        ('set_template', '📋 [HTML] Set IMDb Custom Template for Usage!!'),
        ('choosetheme', '🗄 Set Custom Bot Theme for Usage for Own Decorative Purposes !!'),
        (f'{BotCommands.HelpCommand}', '🆘 Get Help, How to Use and What to Do. . .'),
        (f'{BotCommands.LogCommand}', '🔀 Get the Bot Log [Owner Only]'),
        (f'{BotCommands.TsHelpCommand}', '🌐 Get help for Torrent Search Module'),
    ]

async def start(client, message):
    """/start command"""
    buttons = [
            [
                InlineKeyboardButton('🚦 Bot Stats 🚦', url='https://t.me/FXTorrentz/28'),
                InlineKeyboardButton('🛃 FX Group 🛃', url='https://t.me/+BgIhdNizM61jOGNl'),
            ]
            ]
    reply_markup=InlineKeyboardMarkup(buttons)
    u_men = message.from_user.mention
    start_log_string = f'''
┏ <i>Dear {u_men}</i>,
┃
┃ <i>If You Want To Use Me, You Have To Join {UPDATES_CHANNEL}</i>
┃
┣ <b>NOTE:</b> <code>All The Uploaded Leeched Contents By You Will Be Sent Here In Your Private Chat From Now.</code>
┃
┗━♦️ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL}♦️
'''

    if message.chat.type == enums.ChatType.PRIVATE:
        if LEECH_LOG:
            await message.reply_text(
                start_log_string,
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML,
                quote=True
            )
        else:
            await message.delete()
    else:
        await message.reply_text(
            "**I Am Alive and Working, Send /help to Know How to Use Me !** ✨",
            parse_mode=enums.ParseMode.MARKDOWN,
        )

async def clean_all():
    aria2 = await aria_start()
    aria2.remove_all(True)
    try:
        shutil.rmtree(DOWNLOAD_LOCATION)
    except FileNotFoundError:
        pass

async def restart(client, message:Message):
    ## Inspired from HuzunluArtemis Restart & HEROKU Utils
    if message.from_user.id != OWNER_ID and message.from_user.id not in SUDO_USERS:
        return
    cmd = message.text.split(' ', 1)
    dynoRestart = False
    dynoKill = False
    if len(cmd) == 2:
        dynoRestart = (cmd[1].lower()).startswith('d')
        dynoKill = (cmd[1].lower()).startswith('k')
    if (not HEROKU_API_KEY) or (not HEROKU_APP_NAME):
        LOGGER.info("[ATTENTION] Fill HEROKU_API_KEY & HEROKU_APP_NAME for Using this Feature.")
        dynoRestart = False
        dynoKill = False
    if dynoRestart:
        LOGGER.info("[HEROKU] Dyno Restarting...")
        restart_message = await message.reply_text("__Dyno Restarting...__")
        app.stop()
        if STRING_SESSION:
            userBot.stop()
        heroku_conn = heroku3.from_key(HEROKU_API_KEY)
        appx = heroku_conn.app(HEROKU_APP_NAME)
        appx.restart()
    elif dynoKill:
        LOGGER.info("[HEROKU] Killing Dyno...")
        await message.reply_text("__Killed Dyno__")
        heroku_conn = heroku3.from_key(HEROKU_API_KEY)
        appx = heroku_conn.app(HEROKU_APP_NAME)
        proclist = appx.process_formation()
        for po in proclist:
            appx.process_formation()[po.type].scale(0)
    else:
        LOGGER.info("[HEROKU] Normally Restarting...")
        restart_message = await message.reply_text("__Restarting...__")
        try:
            await clean_all()
        except Exception as err:
            LOGGER.info(f"Restart Clean Error : {err}")
        srun(["pkill", "-f", "extra-api|new-api"])
        srun(["python3", "update.py"])
        with open(".restartmsg", "w") as f:
            f.truncate(0)
            f.write(f"{restart_message.chat.id}\n{restart_message.id}\n")
        os.execl(executable, executable, "-m", "tobrot")

if __name__ == "__main__":
    # Generat Download Directory, if Not Exist !!
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)

    # Bot Restart & Restart Message >>>>>>>>
    utc_now = datetime.datetime.utcnow()
    ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
    ist = ist_now.strftime("<b>📆 𝘿𝙖𝙩𝙚 :</b> <code>%d %B, %Y</code> \n<b>⏰ 𝙏𝙞𝙢𝙚 :</b> <code>%I:%M:%S %p (GMT+05:30)</code>") #Will Fix to Time Zone Format
    if os.path.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
        bot.edit_message_text("Restarted & Updated Successfully!", chat_id, msg_id) #Telegram Sucks ???
        os.remove(".restartmsg")
    elif OWNER_ID:
        try:
            text = f"<b>Bᴏᴛ Rᴇsᴛᴀʀᴛᴇᴅ !!</b>\n\n<b>📊 𝙃𝙤𝙨𝙩 :</b> <code>{SERVER_HOST}</code>\n{ist}\n\n<b>ℹ️ 𝙑𝙚𝙧𝙨𝙞𝙤𝙣 :</b> <code>{__version__}</code>"
            if RDM_QUOTE:
                try:
                    qResponse = requests.get("https://quote-garden.herokuapp.com/api/v3/quotes/random")
                    if qResponse.status_code == 200:
                        qData = qResponse.json() 
                        qText = qData['data'][0]['quoteText']
                        qAuthor = qData['data'][0]['quoteAuthor']
                        #qGenre = qData['data'][0]['quoteGenre']
                        text += f"\n\n📬 𝙌𝙪𝙤𝙩𝙚 :\n\n<b>{qText}</b>\n\n🏷 <i>By {qAuthor}</i>"
                except Exception as q:
                    LOGGER.info("Quote API Error : {q}")
            if AUTH_CHANNEL:
                for i in AUTH_CHANNEL:
                    bot.sendMessage(chat_id=i, text=text, parse_mode=ParseMode.HTML)
        except Exception as e:
            LOGGER.warning(e)
    if SET_BOT_COMMANDS:
        bot.set_my_commands(botcmds)

    # Start The Bot >>>>>>>
    app.start()

    ##############################################################################
    incoming_message_handler = MessageHandler(
        incoming_message_f,
        filters=filters.command(
            [
                BotCommands.LeechCommand, f"{BotCommands.LeechCommand}@{bot.username}",
                BotCommands.ArchiveCommand, f"{BotCommands.ArchiveCommand}@{bot.username}",
                BotCommands.ExtractCommand, f"{BotCommands.ExtractCommand}@{bot.username}",
                GLEECH_COMMAND,
                GLEECH_UNZIP_COMMAND,
                GLEECH_ZIP_COMMAND,
            ]
        )
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_message_handler)
    ##############################################################################
    # AUTO_LEECH = True !!
    #auto_handler = MessageHandler(incoming_message_f, filters=filters.text & filters.chat(chats=AUTH_CHANNEL))
    #app.add_handler(auto_handler)
    ##############################################################################
    incoming_telegram_download_handler = MessageHandler(
        down_load_media_f,
        filters=filters.command([TELEGRAM_LEECH_COMMAND, TELEGRAM_LEECH_UNZIP_COMMAND])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_telegram_download_handler)
    ##############################################################################
    incoming_purge_message_handler = MessageHandler(
        incoming_purge_message_f,
        filters=filters.command(["purge", f"purge@{bot.username}"]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_purge_message_handler)
    ##############################################################################
    incoming_clone_handler = MessageHandler(
        g_clonee,
        filters=filters.command([f"{BotCommands.GCloneCommand}", f"{BotCommands.GCloneCommand}@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_clone_handler)
    ##############################################################################
    incoming_size_checker_handler = MessageHandler(
        check_size_g,
        filters=filters.command([f"{GET_SIZE_G}"]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_size_checker_handler)
    ##############################################################################
    incoming_g_clear_handler = MessageHandler(
        g_clearme,
        filters=filters.command([f"{RENEWME_COMMAND}", f"{RENEWME_COMMAND}@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_g_clear_handler)
    ##############################################################################
    incoming_youtube_dl_handler = MessageHandler(
        incoming_youtube_dl_f,
        filters=filters.command([f"{BotCommands.YtdlCommand}", f"{BotCommands.YtdlCommand}@{bot.username}", f"{GYTDL_COMMAND}", f"{GYTDL_COMMAND}@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_youtube_dl_handler)
    ##############################################################################
    incoming_youtube_playlist_dl_handler = MessageHandler(
        g_yt_playlist,
        filters=filters.command([f"{BotCommands.PytdlCommand}", f"{BotCommands.PytdlCommand}@{bot.username}", GPYTDL_COMMAND])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_youtube_playlist_dl_handler)
    ##############################################################################
    status_message_handler = MessageHandler(
        status_message_f,
        filters=filters.command([f"{BotCommands.StatusCommand}", f"{BotCommands.StatusCommand}@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(status_message_handler)
    ##############################################################################
    cancel_message_handler = MessageHandler(
        cancel_message_f,
        filters=filters.regex(r'^/cancel($|\_([a-z]|[0-9])+($|\@\S+$))')
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(cancel_message_handler)
    ##############################################################################
    exec_message_handler = MessageHandler(
        exec_message_f,
        filters=filters.command(["exec", "exec@{bot.username}"]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(exec_message_handler)
    ##############################################################################
    eval_message_handler = MessageHandler(
        eval_message_f,
        filters=filters.command(["eval", "exec@{bot.username}"]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(eval_message_handler)
    ##############################################################################
    rename_message_handler = MessageHandler(
        rename_tg_file,
        filters=filters.command([f"{BotCommands.RenameCommand}", f"{BotCommands.RenameCommand}@{bot.username}"]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(rename_message_handler)
    ##############################################################################
    upload_document_handler = MessageHandler(
        upload_document_f,
        filters=filters.command([f"{UPLOAD_COMMAND}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(upload_document_handler)
    ##############################################################################
    upload_log_handler = MessageHandler(
        upload_log_file,
        filters=filters.command([f"{BotCommands.LogCommand}", f"{BotCommands.LogCommand}@{bot.username}"]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(upload_log_handler)
    ##############################################################################
    help_text_handler = MessageHandler(
        help_message_f,
        filters=filters.command([f"{BotCommands.HelpCommand}", f"{BotCommands.HelpCommand}@{bot.username}"]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(help_text_handler)
    ##############################################################################
    call_back_button_handler = CallbackQueryHandler(button)
    app.add_handler(call_back_button_handler)
    ##############################################################################
    save_thumb_nail_handler = MessageHandler(
        save_thumb_nail,
        filters=filters.command([f"{BotCommands.SaveCommand}", f"{BotCommands.SaveCommand}@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(save_thumb_nail_handler)
    ##############################################################################
    clear_thumb_nail_handler = MessageHandler(
        clear_thumb_nail,
        filters=filters.command([f"{BotCommands.ClearCommand}", f"{BotCommands.ClearCommand}@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(clear_thumb_nail_handler)
    ##############################################################################
    rclone_config_handler = MessageHandler(
        rclone_command_f, filters=filters.command([f"{RCLONE_COMMAND}", f"{RCLONE_COMMAND}@{bot.username}"])
    )
    app.add_handler(rclone_config_handler)
    ##############################################################################
    upload_as_doc_handler = MessageHandler(
        upload_as_doc,
        filters=filters.command([f"{BotCommands.ToggleDocCommand}", f"{BotCommands.ToggleDocCommand}@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(upload_as_doc_handler)
    ##############################################################################
    upload_as_video_handler = MessageHandler(
        upload_as_video,
        filters=filters.command([f"{BotCommands.ToggleVidCommand}", f"{BotCommands.ToggleVidCommand}@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(upload_as_video_handler)
    ##############################################################################
    get_speed_handler = MessageHandler(
        get_speed,
        filters=filters.command([f"{BotCommands.SpeedCommand}", f"{BotCommands.SpeedCommand}@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(get_speed_handler)
    ##############################################################################
    searchhelp_handler = MessageHandler(
        searchhelp,
        filters=filters.command([f"{BotCommands.TsHelpCommand}", f"{BotCommands.TsHelpCommand}@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(searchhelp_handler)
    ##############################################################################
    mediainfo_handler = MessageHandler(
        mediainfo,
        filters=filters.command([f"{BotCommands.MediaInfoCommand}", f"{BotCommands.MediaInfoCommand}@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(mediainfo_handler)
    ##############################################################################
    restart_handler = MessageHandler(
        restart,
        filters=filters.command(["restart", f"restart@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(restart_handler)
    ##############################################################################
    stats_handler = MessageHandler(
        stats,
        filters=filters.command([f"{BotCommands.StatsCommand}", f"{BotCommands.StatsCommand}@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(stats_handler)
    ##############################################################################
    start_handler = MessageHandler(
        start,
        filters=filters.command(["start", f"start@{bot.username}"])
    )
    app.add_handler(start_handler)
    ##############################################################################
    prefixx_handler = MessageHandler(
        prefix_set,
        filters=filters.command(["setpre", f"setpre@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(prefixx_handler)
    ##############################################################################
    captionn_handler = MessageHandler(
        caption_set,
        filters=filters.command(["setcap", f"setcap@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(captionn_handler)
    ##############################################################################
    url_parse_handler = MessageHandler(
        url_parser,
        filters=filters.command(["parser", f"parser@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(url_parse_handler)
    ##############################################################################
    imdb_handler = MessageHandler(
        imdb_search,
        filters=filters.command(["imdb", f"imdb@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(imdb_handler)
    ##############################################################################
    template_handler = MessageHandler(
        template_set,
        filters=filters.command(["set_template", f"set_template@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(template_handler)
    ##############################################################################
    ind_scrape_handler = MessageHandler(
        index_scrape,
        filters=filters.command([f"{INDEX_SCRAPE}", f"{INDEX_SCRAPE}@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(ind_scrape_handler)
    ##############################################################################
    user_theme_handler = MessageHandler(
        theme_set,
        filters=filters.command([f"choosetheme", f"choosetheme@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(user_theme_handler)
    ##############################################################################
    user_set_handler = MessageHandler(
        user_settings,
        filters=filters.command([f"currsettings", f"currsettings@{bot.username}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(user_set_handler)

    logging.info(r'''
________    ______           ______                 ______ ____  __
___  __/_______  /____       ___  / ___________________  /___  |/ /
__  /  _  _ \_  /_  _ \________  /  _  _ \  _ \  ___/_  __ \_    / 
_  /   /  __/  / /  __//_____/  /___/  __/  __/ /__ _  / / /    |  
/_/    \___//_/  \___/       /_____/\___/\___/\___/ /_/ /_//_/|_|
    ''')
    logging.info(f"{(app.get_me()).first_name} [@{(app.get_me()).username}] Has Started Running...🏃💨💨")
    if STRING_SESSION:
        logging.info(f"User : {(userBot.get_me()).first_name} Has Started Revolving...♾️⚡️")

    idle()

    app.stop()
    if STRING_SESSION:
        userBot.stop()
