import youtube_dl
import urllib
import discord
import os
import uuid

class dlLog(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

async def conversionCb(file, client, target):
    try:
        await client.send_file(target, file)
    except:
        pass

async def sendWrap(a, b, c):
    try:
        await a.send_message(b, c)
    except:
        pass

ytdlOptions = {
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3"
    }],
    "logger": dlLog()
}

async def downloadMessage(url, targetFolder, client, target):
    parsedUrl = urllib.parse.urlparse(url)
    if all([parsedUrl.scheme, parsedUrl.netloc, parsedUrl.path]):
        options = ytdlOptions
        options["outtmpl"] = targetFolder + "%(title)s" + uuid.uuid4().hex + ".%(ext)s"
        
        dl = youtube_dl.YoutubeDL(options)
        
        ass = dl.prepare_filename(dl.extract_info(url, download=False))
        finalFilename = ass[:ass.rfind('.')+1] + options["postprocessors"][0]["preferredcodec"]

        await sendWrap(client, target, "Downloading and processing " + finalFilename[len(targetFolder) - len(finalFilename):])

        dl.download([parsedUrl.geturl()])
        await conversionCb(finalFilename, client, target)
        os.remove(finalFilename)
    else:
        await sendWrap(client, target, "Request processing failed")
