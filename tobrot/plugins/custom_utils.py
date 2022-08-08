#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) 5MysterySD
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

from pyrogram import enums
from tobrot import LOGGER, DB_URI
from tobrot.database.db_func import DatabaseManager

PRE_DICT = {}
CAP_DICT = {}
IMDB_TEMPLATE = {}

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

    pre_text = await lm.edit_text(f"⚡️<i><b>Custom Prefix Set Successfully</b></i> ⚡️ \n\n👤 <b>User :</b> {u_men}\n🆔 <b>User ID :</b> <code>{user_id_}</code>\n🗃 <b>Prefix :</b> <code>{txt}</code>", parse_mode=enums.ParseMode.HTML)
    

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
    cap_text = await lk.edit_text(f"⚡️<i><b>Custom Caption Set Successfully</b></i> ⚡️ \n\n👤 <b>User :</b> {u_men}\n🆔 <b>User ID :</b> <code>{user_id_}</code>\n🗃 <b>Caption :</b>\n<code>{txt}</code>", parse_mode=enums.ParseMode.HTML)


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
    if txt == "":
        await lm.edit_text("`Send Custom TEMPLATE for your Usage`")
        return
    else:
        template_ = txt
        IMDB_TEMPLATE[user_id_] = template_
    
        await lm.edit_text(f"⚡️<i><b>Custom Template Set Successfully</b></i> ⚡️ \n\n👤 <b>User :</b> {u_men}\n🆔 <b>User ID :</b> <code>{user_id_}</code>\n🗃 <b>IMDB Template :</b> \n<code>{txt}</code>", parse_mode=enums.ParseMode.HTML)
