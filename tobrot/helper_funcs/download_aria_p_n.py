#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | MaxxRider | 5MysterySD
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

import asyncio
import os
import sys
import time
import aria2p
from subprocess import check_output
from pyrogram.errors import FloodWait, MessageNotModified
from tobrot import (
    ARIA_TWO_STARTED_PORT,
    CUSTOM_FILE_NAME,
    EDIT_SLEEP_TIME_OUT,
    LOGGER,
    UPDATES_CHANNEL, 
    MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START,
    CLONE_COMMAND_G
)
from tobrot.helper_funcs.create_compressed_archive import (
    create_archive,
    get_base_name,
    unzip_me,
)
from tobrot.helper_funcs.upload_to_tg import upload_to_gdrive, upload_to_tg
from tobrot.helper_funcs.download import download_tg

from tobrot.helper_funcs.direct_link_generator import url_link_generate
from tobrot.helper_funcs.exceptions import DirectDownloadLinkException
from tobrot.plugins.custom_utils import *
from tobrot.plugins import is_appdrive_link, is_gdtot_link, is_hubdrive_link 
from tobrot.helper_funcs.display_progress import TimeFormatter
sys.setrecursionlimit(10 ** 4)

async def aria_start():
    TRACKERS = check_output("curl -Ns https://raw.githubusercontent.com/XIU2/TrackersListCollection/master/all.txt https://ngosang.github.io/trackerslist/trackers_all_http.txt https://newtrackon.com/api/all https://raw.githubusercontent.com/hezhijie0327/Trackerslist/main/trackerslist_tracker.txt | awk '$0' | tr '\n\n' ','", shell=True).decode('utf-8').rstrip(',')
    aria2_daemon_start_cmd = ["extra-api", "--conf-path=/app/tobrot/aria2/aria2.conf", f"--rpc-listen-port={ARIA_TWO_STARTED_PORT}", f"--bt-stop-timeout={MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START}", f"--bt-tracker=[{TRACKERS}]"]
    #f"--dir={DOWNLOAD_LOCATION}", "--disk-cache=0", "--seed-ratio=0.01"
    LOGGER.info("[ARIA2C] Daemon Initiated ")

    process = await asyncio.create_subprocess_exec(
        *aria2_daemon_start_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()

    aria2 = aria2p.API(
        aria2p.Client(host="http://localhost",
                      port=ARIA_TWO_STARTED_PORT, secret="")
    )
    return aria2

def add_magnet(aria_instance, magnetic_link, c_file_name):
    options = None
    try:
        download = aria_instance.add_magnet(magnetic_link, options=options)
    except Exception as e:
        return (
            False,
            "⛔ **FAILED** ⛔ \n" + str(e) + " \n<b>⌧ Your link is Dead ⚰ .</b>",
        )
    else:
        return True, "" + download.gid + ""


def add_torrent(aria_instance, torrent_file_path):
    if torrent_file_path is None:
        return (
            False,
            "⛔ **FAILED** ⛔ \n"
            + str(e)
            + " \n⌧ <i>Something went Wrong when trying to add <u>TORRENT</u> file to Status.</i>",
        )
    if os.path.exists(torrent_file_path):
        # Add Torrent Into Queue
        try:
            download = aria_instance.add_torrent(
                torrent_file_path, uris=None, options=None, position=None
            )
        except Exception as e:
            return (
                False,
                "⛔ **FAILED** ⛔ \n"
                + str(e)
                + " \n<b>⌧ Your Link is Slow to Process .</b>",
            )
        else:
            return True, "" + download.gid + ""
    else:
        return False, "⛔ **FAILED** ⛔ \n⌧ Please try other sources to get workable link to Process . . ."


def add_url(aria_instance, text_url, c_file_name):
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
        return (
            False,
            f"⛔ **FAILED** ⛔ \n\n⌧ <i>Please do not send Drive links to Process with this Command. Use /{CLONE_COMMAND_G} for Cloning the Link, then Use the Index Link !!</i>",
        )
    elif "mega.nz" in text_url or "mega.co.nz" in text_url:
        return (
            False,
            "⛔ **FAILED** ⛔ \n\n⌧ <i>Please do not send Mega links . I am yet not able to Process Those !!</i>",
        )
    elif is_gdtot_link(text_url) or is_hubdrive_link(text_url) or is_appdrive_link(text_url):
        return (
            False,
            "⛔ **FAILED** ⛔ \n\n⌧ <i>Please Use /parser to Process the Links.</i>",
        )
    else:
        uris = [text_url]
    # Add URL Into Queue
    try:
        download = aria_instance.add_uris(uris, options=options)
    except Exception as e:
        return (
            False,
            "⛔ **FAILED** ⛔ \n" +
            str(e) + " \n\n⌧ <i>Please do not send Slow links to Process.</i>",
        )
    else:
        return True, "" + download.gid + ""


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
            sagtus, err_message = add_magnet(
                aria_instance, incoming_link, c_file_name)
        elif incoming_link.lower().endswith(".torrent"):
            sagtus, err_message = add_torrent(aria_instance, incoming_link)
        else:
            sagtus, err_message = add_url(
                aria_instance, incoming_link, c_file_name)
        if not sagtus:
            return sagtus, err_message
        LOGGER.info(err_message)
        await check_progress_for_dl(
            aria_instance, err_message, sent_message_to_update_tg_p, None
        )
        if incoming_link.startswith("magnet:"):
            err_message = await check_metadata(aria_instance, err_message)
            await asyncio.sleep(1)
            if err_message is not None:
                await check_progress_for_dl(
                    aria_instance, err_message, sent_message_to_update_tg_p, None
                )
            else:
                return False, "can't get metadata \n\n#MetaDataError"
        await asyncio.sleep(1)
        try:
            file = aria_instance.get_download(err_message)
        except aria2p.client.ClientException as ee:
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
            if os.path.exists(check_ifi_file):
                to_upload_file = check_ifi_file
        except Exception as ge:
            LOGGER.info(ge)
            LOGGER.info(
                f"Can't extract {os.path.basename(to_upload_file)}, Uploading the same file"
            )

    if to_upload_file:
        prefix = PRE_DICT.get(user_message.from_user.id, "")
        CUSTOM_FILE_NAME = prefix

        if CUSTOM_FILE_NAME != "":
            if os.path.isfile(to_upload_file):
                os.rename(to_upload_file,
                          f"{CUSTOM_FILE_NAME}{to_upload_file}")
                to_upload_file = f"{CUSTOM_FILE_NAME}{to_upload_file}"
            else:
                for root, _, files in os.walk(to_upload_file):
                    LOGGER.info(files)
                    for org in files:
                        p_name = f"{root}/{org}"
                        n_name = f"{root}/{CUSTOM_FILE_NAME}{org}"
                        os.rename(p_name, n_name)
                to_upload_file = to_upload_file

    if cstom_file_name:
        os.rename(to_upload_file, cstom_file_name)
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
            start_upload = time.time()
            final_response = await upload_to_tg(
                sent_message_to_update_tg_p, to_upload_file, user_id, response, client
            )
            end_upload = time.time()
            if not final_response:
                return True, None
            try:
                timeuti = TimeFormatter((end_upload - start_upload) * 1000)
                message_to_send = ""
                mention_req_user = f"┏ 🗃 𝙇𝙚𝙚𝙘𝙝 𝘾𝙤𝙢𝙥𝙡𝙚𝙩𝙚 !! 🗃\n┃\n┣ 👤 𝐔𝐬𝐞𝐫 : {u_men} ( #ID{user_id} )\n┣⏳️ 𝐓𝐢𝐦𝐞 𝐓𝐚𝐤𝐞𝐧 : {timeuti}\n┃\n"
                message_credits = f"┃\n┃ #FXUploads\n┃\n┗━♦️ℙ𝕠𝕨𝕖𝕣𝕖𝕕 𝔹𝕪 {UPDATES_CHANNEL}♦️"
                for key_f_res_se in final_response:
                    local_file_name = key_f_res_se
                    message_id = final_response[key_f_res_se]
                    channel_id = str(sent_message_to_update_tg_p.chat.id)[4:]
                    private_link = f"https://t.me/c/{channel_id}/{message_id}"
                    message_to_send += f"┣ ⇒ <a href='{private_link}'>{local_file_name}</a>\n"
                    if len(mention_req_user.encode('utf-8') + message_to_send.encode('utf-8') + message_credits.encode('utf-8')) > 4000:
                        time.sleep(1.5)
                        await user_message.reply_text(
                            text=mention_req_user + message_to_send + message_credits, quote=True, disable_web_page_preview=True
                        )
                        message_to_send = ""
                if message_to_send != "":
                    time.sleep(1.5)
                    await user_message.reply_text(
                        text=mention_req_user + message_to_send + message_credits, quote=True, disable_web_page_preview=True
                    )
            except Exception as go:
                LOGGER.error(go)
    return True, None


# https://github.com/jaskaranSM/UniBorg/blob/6d35cf452bce1204613929d4da7530058785b6b1/stdplugins/aria.py#L136-L164
# todo- so much unwanted code, I will remove in future after some testing

async def check_progress_for_dl(aria2, gid, event, previous_message):
    while True:
        try:
            file = aria2.get_download(gid)
            complete = file.is_complete
            is_file = file.seeder
            if not complete:
                if not file.error_message:
                    if file.has_failed:
                        LOGGER.info(
                            f"⛔ Cancel Downloading . .⛔ \n\n ⌧ <i>FileName: `{file.name}` \n⌧ May Be Due to Slow Torrent (Less Seeds to Process).</i>"
                        )
                        await event.reply(
                            f"⛔ Download Cancelled ⛔ :\n\n⌧ <i>FileName: </i><code>{file.name}</code>\n\n #MetaDataError", quote=True
                        )
                        file.remove(force=True, files=True)
                        return
                else:
                    msg = file.error_message
                    LOGGER.info(msg)
                    await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
                    await event.reply(f"`{msg}`")
                    return
                await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
                # await check_progress_for_dl(aria2, gid, event, previous_message)
            else:
                LOGGER.info(
                    f"✅ <i>Downloaded Successfully</i> ✅: `{file.name} ({file.total_length_string()})` "
                )
                # await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
                if not file.is_metadata:
                    await event.edit(
                        f"<b>🔰Status: <i>Downloaded 📥</i></b>:\n\n📨 <b><i>File Name</i></b>: \n`{file.name}`\n\n🗃 <b><i>Total Size</i></b>: 《 `{file.total_length_string()}` 》\n\n #Downloaded" 
                    )
                return
        except aria2p.client.ClientException:
            await event.reply(
                f"<i>⛔ Download Cancelled ⛔</i> :\n<code>{file.name} ({file.total_length_string()})</code>", quote=True
            )
            return
        except MessageNotModified as ep:
            LOGGER.info(ep)
            await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
            # await check_progress_for_dl(aria2, gid, event, previous_message)
            return
        except FloodWait as e:
            LOGGER.info(f"FloodWait : Sleeping {e.value}s")
            time.sleep(e.value)
        except Exception as e:
            LOGGER.info(str(e))
            if "not found" in str(e) or "'file'" in str(e):
                await event.edit(
                    f"<i>⛔ Download Cancelled ⛔</i> :\n<code>{file.name} ({file.total_length_string()})</code>"
                )
                return
            else:
                LOGGER.info(str(e))
                await event.edit(
                    "⛔ <u>ERROR</u> ⛔ :\n<code>{}</code> \n\n#Error".format(str(e))
                )
                return


# https://github.com/jaskaranSM/UniBorg/blob/6d35cf452bce1204613929d4da7530058785b6b1/stdplugins/aria.py#L136-L164
async def check_metadata(aria2, gid):
    file = aria2.get_download(gid)

    if not file.followed_by_ids:
        return None
    new_gid = file.followed_by_ids[0]
    LOGGER.info("Changing GID " + gid + " to " + new_gid)
    return new_gid
