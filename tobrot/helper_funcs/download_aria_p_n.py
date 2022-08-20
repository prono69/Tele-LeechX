#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | MaxxRider | 5MysterySD
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

import sys
from urllib.request import urlretrieve
from asyncio import create_subprocess_exec, subprocess, sleep as asleep
from os import path as opath, rename as orename, walk as owalk
from time import sleep as tsleep, time
from aria2p import API as ariaAPI, Client as ariClient, client as aria2pclient
from subprocess import check_output
from pyrogram.errors import FloodWait, MessageNotModified
from tobrot import (
    ARIA_TWO_STARTED_PORT,
    CUSTOM_FILE_NAME,
    EDIT_SLEEP_TIME_OUT,
    LOGGER,
    UPDATES_CHANNEL, 
    MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START,
    CLONE_COMMAND_G,
    user_settings_lock,
    user_settings
)
from tobrot.helper_funcs.create_compressed_archive import (
    create_archive,
    get_base_name,
    unzip_me,
)
from tobrot.helper_funcs.upload_to_tg import upload_to_gdrive, upload_to_tg
from tobrot.helper_funcs.download import download_tg
from tobrot.bot_theme.themes import BotTheme
from tobrot.helper_funcs.direct_link_generator import url_link_generate
from tobrot.helper_funcs.exceptions import DirectDownloadLinkException
from tobrot.plugins.custom_utils import *
from tobrot.plugins import is_appdrive_link, is_gdtot_link, is_hubdrive_link 
from tobrot.helper_funcs.display_progress import TimeFormatter

sys.setrecursionlimit(10 ** 4)

async def aria_start():
    TRACKERS = check_output("curl -Ns https://raw.githubusercontent.com/XIU2/TrackersListCollection/master/all.txt https://ngosang.github.io/trackerslist/trackers_all_http.txt https://newtrackon.com/api/all https://raw.githubusercontent.com/hezhijie0327/Trackerslist/main/trackerslist_tracker.txt | awk '$0' | tr '\n\n' ','", shell=True).decode('utf-8').rstrip(',')
    aria2_daemon_start_cmd = ["chrome", "--conf-path=/app/tobrot/aria2/aria2.conf", f"--rpc-listen-port={ARIA_TWO_STARTED_PORT}", f"--bt-stop-timeout={MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START}", f"--bt-tracker=[{TRACKERS}]"]
    #f"--dir={DOWNLOAD_LOCATION}", "--disk-cache=0", "--seed-ratio=0.01"
    LOGGER.info("[ARIA2C] Daemon Initiated ")

    process = await create_subprocess_exec(
        *aria2_daemon_start_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()

    return ariaAPI(
        ariClient(
            host="http://localhost", port=ARIA_TWO_STARTED_PORT, secret=""
        )
    )

def add_magnet(aria_instance, magnetic_link, c_file_name, user_msg):
    options = None
    try:
        download = aria_instance.add_magnet(magnetic_link, options=options)
        with user_settings_lock:
            user_settings[download.gid] = user_msg
    except Exception as e:
        return False, f"⛔ **FAILED** ⛔ \n\n<b>⌧ Your link is Dead Maybe ⚰ .\n{e}</b>"
    else:
        return True, download.gid

def add_torrent(aria_instance, torrent_file_path, user_msg):
    if torrent_file_path is None:
        return False, "⛔ **FAILED** ⛔\n\n⌧ <i>Something went Wrong when trying to add <u>TORRENT</u> file to Status.</i>"
    if opath.exists(torrent_file_path):
        try:
            download = aria_instance.add_torrent(torrent_file_path, uris=None, options=None, position=None)
            with user_settings_lock:
                user_settings[download.gid] = user_msg
        except Exception as e:
            return False, f"⛔ **FAILED** ⛔ \n\n<b>⌧ Your Link is Slow to Process .</b>\n⌧ {e}"
        else:
            return True, download.gid
    elif (torrent_file_path.lower()).startswith("https") and (not opath.exists(torrent_file_path)):
        torrent_file_name = (torrent_file_path.split('/'))[-1]
        urlretrieve(torrent_file_path, f"/app/{torrent_file_name}")
        try:
            sagtus, err_message = add_torrent(aria_instance, torrent_file_name, user_msg)
        except Exception as e:
            return False, f"⛔ **FAILED** ⛔ \n\n<b>⌧ Your Link is Slow to Process .</b>\n⌧ {e}"
        else:
            return True, err_message
    else:
        return False, "⛔ **FAILED** ⛔ \n⌧ Please try other sources to get workable link to Process . . ."

def add_url(aria_instance, text_url, c_file_name, user_msg):
    options = None
    uris = None
    if "zippyshare.com" in text_url \
        or "osdn.net" in text_url \
        or "mediafire.com" in text_url \
        or "https://uptobox.com" in text_url \
        or "cloud.mail.ru" in text_url \
        or "github.com" in text_url \
        or "yadi.sk" in text_url  \
        or "hxfile.co" in text_url  \
        or "https://anonfiles.com" in text_url  \
        or "letsupload.io" in text_url  \
        or "fembed.net" in text_url  \
        or "fembed.com" in text_url  \
        or "femax20.com" in text_url  \
        or "fcdn.stream" in text_url  \
        or "feurl.com" in text_url  \
        or "naniplay.nanime.in" in text_url  \
        or "naniplay.nanime.biz" in text_url  \
        or "naniplay.com" in text_url  \
        or "layarkacaxxi.icu" in text_url  \
        or "sbembed.com" in text_url  \
        or "streamsb.net" in text_url  \
        or "sbplay.org" in text_url  \
        or "1drv.ms" in text_url  \
        or "pixeldrain.com" in text_url  \
        or "antfiles.com" in text_url  \
        or "streamtape.com" in text_url  \
        or "https://bayfiles.com" in text_url  \
        or "1fichier.com" in text_url  \
        or "solidfiles.com" in text_url  \
        or "krakenfiles.com" in text_url  \
        or "gplinks.co" in text_url  \
        or "racaty.net" in text_url:
            try:
                urisitring = url_link_generate(text_url)
                uris = [urisitring]
            except DirectDownloadLinkException as e:
                LOGGER.info(f'{text_url}: {e}')
    elif "drive.google.com" in text_url:
        return False, f"⛔ **FAILED** ⛔ \n\n⌧ <i>Please do not send Drive links to Process with this Command. Use /{CLONE_COMMAND_G} for Cloning the Link, then Use the Index Link !!</i>"
    elif "mega.nz" in text_url or "mega.co.nz" in text_url:
        return False, "⛔ **FAILED** ⛔ \n\n⌧ <i>Please do not send Mega links . I am yet not able to Process Those !!</i>"
    elif is_gdtot_link(text_url) or is_hubdrive_link(text_url) or is_appdrive_link(text_url):
        return False, "⛔ **FAILED** ⛔ \n\n⌧ <i>Please Use /parser to Process the Links.</i>"
    else:
        uris = [text_url]

    try:
        download = aria_instance.add_uris(uris, options=options)
        with user_settings_lock:
            user_settings[download.gid] = user_msg
    except Exception as e:
        return False, f"⛔ **FAILED** ⛔ \n\n⌧ <i>Please do not send Slow links to Process.</i>\n{e}"
    else:
        return True, download.gid

async def call_apropriate_function(
    aria_instance,
    incoming_link,
    c_file_name,
    sent_message_to_update_tg_p,
    is_zip,
    cstom_file_name,
    is_cloud,
    is_unzip,
    is_file,
    user_message,
    client,
):
    if not is_file:

        if incoming_link.lower().startswith("magnet:"):
            sagtus, err_message = add_magnet(aria_instance, incoming_link, c_file_name, user_message)
        elif incoming_link.lower().endswith(".torrent"):
            sagtus, err_message = add_torrent(aria_instance, incoming_link, user_message)
        else:
            sagtus, err_message = add_url(aria_instance, incoming_link, c_file_name, user_message)

        if not sagtus:
            return sagtus, err_message
        LOGGER.info(err_message)

        await check_progress_for_dl(
            aria_instance, err_message, sent_message_to_update_tg_p, None, user_message
        )
        if incoming_link.startswith("magnet:"):
            err_message = await check_metadata(aria_instance, err_message)
            await asleep(1)
            if err_message is not None:
                await check_progress_for_dl(
                    aria_instance, err_message, sent_message_to_update_tg_p, None, user_message
                )
            else:
                return False, "can't get metadata \n\n#MetaDataError"
        await asleep(1)
        try:
            file = aria_instance.get_download(err_message)
        except aria2pclient.ClientException as ee:
            LOGGER.error(ee)
            return True, None
        to_upload_file = file.name
        com_g = file.is_complete
    else:
        await sent_message_to_update_tg_p.delete()
        to_upload_file, sent_message_to_update_tg_p = await download_tg(client=client, message=user_message)
        if not to_upload_file:
            return True, None
        com_g = True

    LOGGER.info(f" Zip : {is_zip}")
    LOGGER.info(f" UnZip : {is_unzip}")

    if is_zip:
        check_if_file = await create_archive(to_upload_file)
        if check_if_file is not None:
            to_upload_file = check_if_file

    if is_unzip:
        try:
            check_ifi_file = get_base_name(to_upload_file)
            await unzip_me(to_upload_file)
            if opath.exists(check_ifi_file):
                to_upload_file = check_ifi_file
        except Exception as ge:
            LOGGER.info(ge)
            LOGGER.info(
                f"Can't extract {opath.basename(to_upload_file)}, Uploading the same file"
            )
    u_id = user_message.from_user.id
    if to_upload_file:
        prefix = PRE_DICT.get(u_id, "")
        CUSTOM_FILE_NAME = prefix

        if CUSTOM_FILE_NAME != "":
            if opath.isfile(to_upload_file):
                if not to_upload_file.startswith(CUSTOM_FILE_NAME):
                    orename(to_upload_file, f"{CUSTOM_FILE_NAME}{to_upload_file}")
                    to_upload_file = f"{CUSTOM_FILE_NAME}{to_upload_file}"
            else:
                for root, _, files in owalk(to_upload_file):
                    for org in files:
                        p_name = f"{root}/{org}"
                        if not org.startswith(CUSTOM_FILE_NAME):
                            n_name = f"{root}/{CUSTOM_FILE_NAME}{org}"
                            orename(p_name, n_name)
                to_upload_file = to_upload_file

    if cstom_file_name:
        orename(to_upload_file, cstom_file_name)
        to_upload_file = cstom_file_name

    response = {}

    u_men = user_message.from_user.mention 
    user_id = user_message.from_user.id
    if com_g:
        if is_cloud:
            await upload_to_gdrive(
                to_upload_file, sent_message_to_update_tg_p, user_message, user_id
            )
        else:
            start_upload = time()
            final_response = await upload_to_tg(
                sent_message_to_update_tg_p, to_upload_file, user_id, response, client
            )
            end_upload = time()
            if not final_response:
                return True, None
            try:
                timeuti = TimeFormatter((end_upload - start_upload) * 1000)
                message_to_send = ""
                mention_req_user = ((BotTheme(u_id)).TOP_LIST_FILES_MSG).format(
                    user_id = u_id,
                    u_men = u_men,
                    timeuti = timeuti
                )                
                message_credits = ((BotTheme(u_id)).BOTTOM_LIST_FILES_MSG).format(
                    UPDATES_CHANNEL = UPDATES_CHANNEL
                )
                for key_f_res_se in final_response:
                    local_file_name = key_f_res_se
                    message_id = final_response[key_f_res_se]
                    channel_id = str(sent_message_to_update_tg_p.chat.id)[4:]
                    private_link = f"https://t.me/c/{channel_id}/{message_id}"
                    message_to_send += ((BotTheme(u_id)).SINGLE_LIST_FILES_MSG).format(
                        private_link = private_link,
                        local_file_name = local_file_name
                    )
                    if len(mention_req_user.encode('utf-8') + message_to_send.encode('utf-8') + message_credits.encode('utf-8')) > 4000:
                        tsleep(1.5)
                        await user_message.reply_text(
                            text=mention_req_user + message_to_send + message_credits, quote=True, disable_web_page_preview=True
                        )
                        message_to_send = ""
                if message_to_send != "":
                    tsleep(1.5)
                    await user_message.reply_text(
                        text=mention_req_user + message_to_send + message_credits, quote=True, disable_web_page_preview=True
                    )
            except Exception as go:
                LOGGER.error(go)
    return True, None


# https://github.com/jaskaranSM/UniBorg/blob/6d35cf452bce1204613929d4da7530058785b6b1/stdplugins/aria.py#L136-L164
async def check_progress_for_dl(aria2, gid, event, previous_message, user_message):
    while True:
        try:
            file = aria2.get_download(gid)
            complete = file.is_complete
            is_file = file.seeder
            if not complete:
                if not file.error_message:
                    if file.has_failed:
                        LOGGER.info(f"⛔ Cancel Downloading . .⛔ \n\n ⌧ <i>FileName: `{file.name}` \n⌧ May Be Due to Slow Torrent (Less Seeds to Process).</i>")
                        await event.reply(
                            f"⛔ Download Cancelled ⛔ :\n\n⌧ <i>FileName: </i><code>{file.name}</code>\n\n #MetaDataError", quote=True
                        )
                        file.remove(force=True, files=True)
                        return
                else:
                    msg = file.error_message
                    LOGGER.info(msg)
                    await asleep(EDIT_SLEEP_TIME_OUT)
                    await event.reply(f"`{msg}`")
                    return
                await asleep(EDIT_SLEEP_TIME_OUT)
                # await check_progress_for_dl(aria2, gid, event, previous_message)
            else:
                LOGGER.info(
                    f"Downloaded Successfully : `{file.name} ({file.total_length_string()})` "
                )
                if not file.is_metadata:
                    await event.edit(((BotTheme(user_message.from_user.id)).DOWN_COM_MSG).format(
                        filename = file.name,
                        size = file.total_length_string()
                    ))
                return
        except aria2pclient.ClientException:
            await event.reply(f"<i>⛔ Download Cancelled ⛔</i> :\n<code>{file.name} ({file.total_length_string()})</code>", quote=True)
            return
        except MessageNotModified as ep:
            LOGGER.info(ep)
            await asleep(EDIT_SLEEP_TIME_OUT)
            # await check_progress_for_dl(aria2, gid, event, previous_message)
            return
        except FloodWait as e:
            LOGGER.info(f"FloodWait : Sleeping {e.value}s")
            tsleep(e.value)
        except Exception as e:
            LOGGER.info(str(e))
            if "not found" in str(e) or "'file'" in str(e):
                await event.edit(
                    f"<i>⛔ Download Cancelled ⛔</i> :\n<code>{file.name} ({file.total_length_string()})</code>"
                )
            else:
                LOGGER.info(str(e))
                await event.edit(f"⛔ <u>ERROR</u> ⛔ :\n<code>{e}</code> \n\n#Error")

            return

async def check_metadata(aria2, gid):
    file = aria2.get_download(gid)

    if not file.followed_by_ids:
        return None
    new_gid = file.followed_by_ids[0]
    with user_settings_lock:
        user_settings[new_gid] = user_settings.pop(gid)
    LOGGER.info(f"Changing GID : {gid} to {new_gid}")
    return new_gid
