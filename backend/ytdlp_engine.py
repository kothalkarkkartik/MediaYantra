import yt_dlp
from utils.ffmpeg_utils import get_ffmpeg_path

def get_video_info(url):
    ydl_opts = {
        'skip_download': True,
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False
    }
    
    ffmpeg_location = get_ffmpeg_path()
    if ffmpeg_location:
        ydl_opts['ffmpeg_location'] = ffmpeg_location

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return info
        except Exception as e:
            raise Exception(f"Failed to fetch metadata: {str(e)}")

def get_playlist_info(url):
    ydl_opts = {
        'skip_download': True,
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True # Flat extract for playlists is faster
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return info
        except Exception as e:
            raise Exception(f"Failed to fetch playlist: {str(e)}")
