#!/usr/bin/env python
#
# Semaphore: A simple (rule-based) bot library for Signal Private Messenger.
# Copyright (C) 2021 Lazlo Westerhof <semaphore@lazlo.me>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
Signal Bot example, archive photo to IPFS.
"""
import traceback
import json
import mimetypes
import logging
import os
from pathlib import Path
import io
import anyio
import requests
import shutil

from semaphore import Bot, ChatContext



def proofmode_process(filepath,metadata):
    filepath = "/var/run" + filepath
    target_file_base = "/store/" + os.path.basename(filepath) 
    with open(target_file_base + ".json", 'w') as f:
        f.write(json.dumps(metadata))
    shutil.copyfile(filepath, target_file_base + ".zip")

    return ""


async def proofmode(ctx: ChatContext) -> None:
    global Latest_photo

    
    logging.log(logging.INFO,">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    logging.log(logging.INFO,"data message: {}".format(ctx.message.data_message))
    meta = {
        "target": str(ctx.message.username),
        "source": str(ctx.message.source.number),
        "source_uuid": str(ctx.message.source.uuid),
        "timestamp": str(ctx.message.timestamp),
        "timestampServer": str(ctx.message.server_timestamp),
        "body": str(ctx.message.data_message.body),
    }
    logging.log(logging.INFO,"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    try:
        await ctx.message.mark_read()
        await ctx.message.typing_started()
        logging.log(logging.INFO,"Procesing " + str(len(ctx.message.data_message.attachments)) + " attachments")
        if len(ctx.message.data_message.attachments) > 0:
            
            logging.log(logging.INFO,"found " + str(len(ctx.message.data_message.attachments)))
            for attachment in ctx.message.data_message.attachments:
                await ctx.message.reply(body="📎", reaction=True)
                if attachment.content_type in ["application/zip"]:
                    proofmode_process(attachment.stored_filename,meta)
                await ctx.message.reply(body="💾", reaction=True)                
                logging.log(logging.INFO,f"{attachment.content_type} ")
        else:
                # echo
                await ctx.message.reply(body="❓", reaction=True)        
        await ctx.message.typing_stopped()
    except  Exception:
        logging.log(logging.INFO,traceback.format_exc())

async def main():
    """Start the bot."""
    # Connect the bot to number.
    async with Bot(os.environ["SIGNAL_PHONE_NUMBER"]) as bot:
        bot.register_handler("", proofmode)

        # Run the bot until you press Ctrl-C.
        await bot.start()


if __name__ == '__main__':
    anyio.run(main)
