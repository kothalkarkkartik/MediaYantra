import os
import sys

try:
    import imageio_ffmpeg
    HAS_IMAGEIO_FFMPEG = True
except ImportError:
    HAS_IMAGEIO_FFMPEG = False

def get_ffmpeg_path():
    """
    Returns the absolute path to ffmpeg.exe using imageio_ffmpeg
    """
    if HAS_IMAGEIO_FFMPEG:
        return imageio_ffmpeg.get_ffmpeg_exe()
    
    return None
