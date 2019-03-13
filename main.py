import discord
import re
import uuid
from threading import Thread
import asyncio

import config
import downloader

downloadDir = "tmp/"

mentionPattern = "\s*((<@&?\d{18}>)|@(everyone|here))\s*"

client = discord.Client()

def formatMsg(content):
    return re.sub(mentionPattern, "", content).strip()

@client.event
async def on_ready():
    print(client.user.name + " has logged in")

@client.event
async def on_message(message):
    if (message.server is not None):
        # in server
        if (client.user.id in message.raw_mentions):
            a = asyncio.get_event_loop()
            a.create_task(downloader.downloadMessage(formatMsg(message.content), downloadDir, client, message.channel))
    else:
        # in pm

        # ??? error is thrown but message is still sent to user 
        a = asyncio.get_event_loop()
        a.create_task(downloader.downloadMessage(formatMsg(message.content), downloadDir, client, message.author))
        pass


client.run(config.botSecret)