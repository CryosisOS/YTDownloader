import os
import sys
import youtube_dl
import re
import shutil

FILEPATH = 'S:/Programming/Personal/Programs/YTDownloader/downloads'

def performRegexCheckForYTMatch(url):
    # Defining the youtube regular expression pattern.
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    # Performing the check.
    youtube_regex_match = re.match(youtube_regex, url)
    # Boolean switch on the re.Match Object.
    if youtube_regex_match is not None:
        return True
    return False

def parseArgs(args):
    if len(args) > 1:
        print("Too many arguments given, expected one.")
        return None
    elif len(args) < 1:
        print("Not enough arguments given, expected one.")
        return None
    elif performRegexCheckForYTMatch(args[0]) is False:
        print("Given URL does not match YouTube URL format.")
        return None
    else:
        return args[0]

def convertFileName(filename):
    filename = filename[::-1]
    filename = filename.replace("mbew", "3pm", 1)
    return filename[::-1]

def createDLFolder():
    if not os.path.exists(FILEPATH):
        os.makedirs(FILEPATH)

def moveFile(filename):
    if os.path.exists(f"{FILEPATH}/{filename}"):
        os.remove(f"{FILEPATH}/{filename}")
    os.rename(filename, f"{FILEPATH}/{filename}")
    shutil.copyfile(f"{FILEPATH}/{filename}", f"M:/music/{filename}")

def __main__():
    args = sys.argv[1:]
    url = parseArgs(args)
    if url is None:
        exit(0)
    createDLFolder()

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        filename = convertFileName(filename)
        moveFile(filename)

if __name__ == "__main__":
    __main__()