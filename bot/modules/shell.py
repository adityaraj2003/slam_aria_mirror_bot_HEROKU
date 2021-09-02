import requests
from telegram.ext import CommandHandler
from telegram import InlineKeyboardMarkup

from bot import Interval, INDEX_URL, BUTTON_FOUR_NAME, BUTTON_FOUR_URL, BUTTON_FIVE_NAME, BUTTON_FIVE_URL, BUTTON_SIX_NAME, BUTTON_SIX_URL, BLOCK_MEGA_FOLDER, BLOCK_MEGA_LINKS, VIEW_LINK
from bot import dispatcher, DOWNLOAD_DIR, DOWNLOAD_STATUS_UPDATE_INTERVAL, download_dict, download_dict_lock, SHORTENER, SHORTENER_API, TAR_UNZIP_LIMIT
from bot.helper.ext_utils import fs_utils, bot_utils
from bot.helper.ext_utils.bot_utils import setInterval, get_mega_link_type
from bot.helper.ext_utils.exceptions import DirectDownloadLinkException, NotSupportedExtractionArchive
from bot.helper.mirror_utils.download_utils.aria2_download import AriaDownloadHelper
from bot.helper.mirror_utils.download_utils.mega_downloader import MegaDownloadHelper
from bot.helper.mirror_utils.download_utils.direct_link_generator import direct_link_generator
from bot.helper.mirror_utils.download_utils.telegram_downloader import TelegramDownloadHelper
from bot.helper.mirror_utils.status_utils import listeners
from bot.helper.mirror_utils.status_utils.extract_status import ExtractStatus
from bot.helper.mirror_utils.status_utils.tar_status import TarStatus
from bot.helper.mirror_utils.status_utils.upload_status import UploadStatus
from bot.helper.mirror_utils.status_utils.gdownload_status import DownloadStatus
from bot.helper.mirror_utils.upload_utils import gdriveTools
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import *
from bot.helper.telegram_helper import button_build
import urllib
import pathlib
import os
import subprocess
import threading
import re
import random
import string
import ffmpeg
import subprocess
from bot import LOGGER, dispatcher
from telegram import ParseMode
from telegram.ext import CommandHandler
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands

def hlsrip(client, message, streamUrl, recordingDuration):
    user_id = message.from_user.id
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%d-%m-%Y-%H:%M:%S')
    replace = ind_time.replace(":", "_")
    video_opts = '-ss 00:00:00 -t'
    video_opts2 = '-acodec copy -bsf:a aac_adtstoasc -vcodec copy'
    filename = f'MarvelHQ_TV_RIP[{replace}].mp4'
    call(['ffmpeg', '-i', streamUrl] + video_opts.split() + [recordingDuration] + video_opts2.split() + [filename])
    return filename   

def shell(update, context):
    message = update.effective_message
    cmd = message.text.split(' ', 1)
    recording_duration = cmd[1]
    cmd = hlsrip(client, message, streamUrl="https://feed.play.mv/live/10005200/niZoVrR2vD/master.m3u8", recordingDuration=f'{recording_duration}')
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%d-%m-%Y-%H:%M:%S')
    replace = ind_time.replace(":", "_")
    filename = f'MarvelHQ_TV_RIP[{replace}].mp4'
    if cmd: 
        drive.upload(cmd)
    
    
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    reply = ''
    stderr = stderr.decode()
    stdout = stdout.decode()
    if stdout:
        reply += f"*Stdout*\n`{stdout}`\n"
        LOGGER.info(f"Shell - {cmd} - {stdout}")
    if stderr:
        reply += f"*Stderr*\n`{stderr}`\n"
        LOGGER.error(f"Shell - {cmd} - {stderr}")
    if len(reply) > 3000:
        with open('shell_output.txt', 'w') as file:
            file.write(reply)
        with open('shell_output.txt', 'rb') as doc:
            context.bot.send_document(
                document=doc,
                filename=doc.name,
                reply_to_message_id=message.message_id,
                chat_id=message.chat_id)
    else:
        message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)
        
     


SHELL_HANDLER = CommandHandler(BotCommands.ShellCommand, shell, 
                                                  filters=CustomFilters.owner_filter, run_async=True)
dispatcher.add_handler(SHELL_HANDLER)
