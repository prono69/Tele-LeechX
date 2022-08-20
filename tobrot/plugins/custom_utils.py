#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) 5MysterySD
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

from pyrogram import enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 

from tobrot import LOGGER, DB_URI, PRE_DICT, CAP_DICT, IMDB_TEMPLATE
from tobrot.database.db_func import DatabaseManager
from tobrot.bot_theme.themes import BotTheme

async def prefix_set(client, message):
    '''  /setpre command '''
    lm = await message.reply_text(
        text="`Setting Up ...`",
    )
    user_id_ = message.from_user.id 
    u_men = message.from_user.mention
    pre_send = message.text.split(" ", maxsplit=1)
    reply_to = message.reply_to_message
    if len(pre_send) > 1:
        txt = pre_send[1]
    elif reply_to is not None:
        txt = reply_to.text
    else:
        txt = ""
    prefix_ = txt
    PRE_DICT[user_id_] = prefix_
    if DB_URI:
        DatabaseManager().user_pre(user_id_, prefix_)
        LOGGER.info(f"[DB] User : {user_id_} Prefix Saved to Database")

    pre_text = await lm.edit_text(((BotTheme(user_id_)).PREFIX_MSG).format(
            u_men = u_men,
            uid = user_id_,
            t = txt
        ), 
        parse_mode=enums.ParseMode.HTML
    )
    

async def caption_set(client, message):
    '''  /setcap command '''

    lk = await message.reply_text(
        text="`Setting Up ...`",
    )
    user_id_ = message.from_user.id 
    u_men = message.from_user.mention
    cap_send = message.text.split(" ", maxsplit=1)
    reply_to = message.reply_to_message
    if len(cap_send) > 1:
        txt = cap_send[1]
    elif reply_to is not None:
        txt = reply_to.text
    else:
        txt = ""
    caption_ = txt
    CAP_DICT[user_id_] = caption_
    if DB_URI:
        DatabaseManager().user_cap(user_id_, caption_)
        LOGGER.info(f"[DB] User : {user_id_} Caption Saved to Database")
    try:
        txx = txt.split("#", maxsplit=1)
        txt = txx[0]
    except:
        pass 
    cap_text = await lk.edit_text(((BotTheme(user_id_)).CAPTION_MSG).format(
            u_men = u_men,
            uid = user_id_,
            t = txt
        ),
        parse_mode=enums.ParseMode.HTML
    )


async def template_set(client, message):
    '''  /set_template command '''
    lm = await message.reply_text(
        text="`Checking Input ...`",
    )
    user_id_ = message.from_user.id 
    u_men = message.from_user.mention
    tem_send = message.text.split(" ", maxsplit=1)
    reply_to = message.reply_to_message
    if len(tem_send) > 1:
        txt = tem_send[1]
    elif reply_to is not None:
        txt = reply_to.text
    else:
        txt = ""
    template_ = txt
    IMDB_TEMPLATE[user_id_] = template_
    if DB_URI:
        DatabaseManager().user_imdb(user_id_, template_)
        LOGGER.info(f"[DB] User : {user_id_} IMDB Template Saved to Database")
    await lm.edit_text(((BotTheme(user_id_)).IMDB_MSG).format(
            u_men = u_men,
            uid = user_id_,
            t = txt
        ),
        parse_mode=enums.ParseMode.HTML
    )

async def theme_set(client, message):
    '''  /choosetheme command '''
    lk = await message.reply_text(
        text="`Fetching Current Themes ...`",
    )
    user_id_ = message.from_user.id 
    u_men = message.from_user.mention

    theme_btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("fx-optimised-theme", callback_data = f"theme {user_id_} fx-optimised-theme")],
        [InlineKeyboardButton("fx-minimal-theme", callback_data = f"theme {user_id_} fx-minimal-theme")],
        [InlineKeyboardButton("fx-random-theme", callback_data = f"theme {user_id_} fx-random-theme")],
        [InlineKeyboardButton("⛔️ Close ⛔️", callback_data = f"close")],
    ])

    await lk.edit_text(((BotTheme(user_id_)).THEME_MSG).format(
            u_men = u_men,
            uid = user_id_
        ),
        parse_mode=enums.ParseMode.HTML, 
        reply_markup=theme_btn
    )
