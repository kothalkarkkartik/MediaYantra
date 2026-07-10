import sys
sys.path.insert(0, r"o:\media yantra")
import yt_dlp
from utils.ffmpeg_utils import get_ffmpeg_path

base_opts = {
    'quiet': True,
    'noprogress': True, 
    'format': 'bestaudio/best',
    'outtmpl': r"o:\media yantra\test_quiet.%(ext)s"
}

def hook(d):
    print("HOOK CAUGHT:", d['status'])

base_opts['progress_hooks'] = [hook]

with yt_dlp.YoutubeDL(base_opts) as ydl:
    ydl.extract_info("https://www.youtube.com/watch?v=jNQXAC9IVRw", download=True)
