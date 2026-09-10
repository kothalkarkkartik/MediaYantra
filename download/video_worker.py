import threading
import sys
import copy
import os
import re
from utils.ffmpeg_utils import get_ffmpeg_path
from utils.logger_util import app_logger
from settings.config import config

class DownloadWorker(threading.Thread):
    def __init__(self, url, options, progress_hook, finished_hook, error_hook):
        super().__init__()
        self.url = url
        self.options = options
        self.progress_hook = progress_hook
        self.finished_hook = finished_hook
        self.error_hook = error_hook
        self._is_cancelled = False
        self.daemon = True
        self.info = None
        
        self._pause_event = threading.Event()
        self._pause_event.set()

    def run(self):
        base_opts = {
            'progress_hooks': [self._internal_hook],
            'quiet': True,
            'no_warnings': True,
            'noprogress': True,
            'logger': app_logger,
            'nooverwrites': True,    # CRITICAL: Prevent deleting existing videos
            'continuedl': True,      # CRITICAL: Resume from where we left off
            'file_access_retries': 20,
            'concurrent_fragment_downloads': 15,    # Enable extreme concurrent multithreading
            'http_chunk_size': 10485760             # 10 MB chunks
        }
        
        ffmpeg_location = get_ffmpeg_path()
        if ffmpeg_location:
            base_opts['ffmpeg_location'] = ffmpeg_location
            
        cb = config.get("cookies_browser", "None")
        if cb and cb != "None":
            base_opts['cookiesfrombrowser'] = (cb.lower(),)
            
        base_opts.update(self.options)
        
        engines = [
             ('yt-dlp (Primary Standard)', self._run_ytdlp, [base_opts]),
             ('yt-dlp (Android Client Fallback)', self._run_ytdlp_android, [base_opts]),
             ('yt-dlp (iOS Client Fallback)', self._run_ytdlp_ios, [base_opts]),
             ('yt-dlp (TV Client Fallback)', self._run_ytdlp_tv, [base_opts]),
             ('youtube-dl (Legacy Fallback)', self._run_youtubedl, [base_opts]),
             ('pytubefix (Python API Fallback)', self._run_pytubefix, [])
        ]
        
        last_err = None
        for name, engine_func, args in engines:
            if self._is_cancelled:
                break
            app_logger.debug(f"Attempting download with engine: {name}")
            try:
                self.info = engine_func(*args)
                if not self._is_cancelled:
                    app_logger.debug(f"Engine {name} succeeded!")
                    self.finished_hook(self.info)
                return  # Exit out upon success!
            except Exception as e:
                app_logger.warning(f"Engine {name} failed: {e}")
                last_err = str(e)
                
        if not self._is_cancelled:
            self.error_hook(f"All 4 engines failed! Last error: {last_err}")

    def _run_ytdlp(self, opts):
        import yt_dlp
        with yt_dlp.YoutubeDL(opts) as ydl:
            return ydl.extract_info(self.url, download=True)
            
    def _run_ytdlp_android(self, opts):
        import yt_dlp
        android_opts = opts.copy()
        android_opts['extractor_args'] = {'youtube': {'client': ['android']}}
        with yt_dlp.YoutubeDL(android_opts) as ydl:
            return ydl.extract_info(self.url, download=True)

    def _run_ytdlp_ios(self, opts):
        import yt_dlp
        ios_opts = opts.copy()
        ios_opts['extractor_args'] = {'youtube': {'client': ['ios']}}
        with yt_dlp.YoutubeDL(ios_opts) as ydl:
            return ydl.extract_info(self.url, download=True)
            
    def _run_ytdlp_tv(self, opts):
        import yt_dlp
        tv_opts = opts.copy()
        tv_opts['extractor_args'] = {'youtube': {'client': ['tv']}}
        with yt_dlp.YoutubeDL(tv_opts) as ydl:
            return ydl.extract_info(self.url, download=True)

    def _run_youtubedl(self, opts):
        import youtube_dl
        ydl_opts = opts.copy()
        ydl_opts.pop('logger', None) # Legacy youtube_dl can conflict with custom loggers
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(self.url, download=True)
            
    def _run_pytubefix(self):
        from pytubefix import YouTube
        
        def _pytube_progress(stream, chunk, bytes_remaining):
            self._pause_event.wait()
            if self._is_cancelled:
                raise Exception("Download Cancelled by User")
            total = stream.filesize
            downloaded = total - bytes_remaining
            percent = (downloaded / total * 100) if total else 0
            self.progress_hook({
                'status': 'downloading',
                'percent': percent,
                'speed': 0, 'eta': 0,
                'downloaded': downloaded,
                'total': total
            })

        yt = YouTube(self.url, on_progress_callback=_pytube_progress)
        
        # Grab best standard resolution (usually 720p with audio)
        stream = yt.streams.get_highest_resolution() 
        if not stream:
            raise Exception("No streams found via pytubefix")
            
        out_tmpl = self.options.get('outtmpl', '')
        # Fallback directory deduction
        out_dir = os.path.dirname(out_tmpl) if out_tmpl else '.'
        if '%(' in out_dir: out_dir = '.'  
        
        title = re.sub(r'[\\/*?:"<>|]', "", yt.title)
        filename = f"{title}.mp4"
        
        stream.download(output_path=out_dir, filename=filename)
        
        self.progress_hook({'status': 'finished', 'filepath': os.path.join(out_dir, filename)})
        return {"title": yt.title, "url": self.url, "thumbnail": yt.thumbnail_url}

    def _internal_hook(self, d):
        self._pause_event.wait()
        
        if self._is_cancelled:
            raise Exception("Download Cancelled by User")
            
        if d['status'] == 'downloading':
            try:
                total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                downloaded_bytes = d.get('downloaded_bytes', 0)
                speed = d.get('speed', 0)
                eta = d.get('eta', 0)
                
                percent = (downloaded_bytes / total_bytes * 100) if total_bytes else 0
                self.progress_hook({
                    'status': 'downloading',
                    'percent': percent,
                    'speed': speed,
                    'eta': eta,
                    'downloaded': downloaded_bytes,
                    'total': total_bytes
                })
            except:
                pass
        elif d['status'] == 'finished':
            self.progress_hook({
                'status': 'finished',
                'filepath': d.get('filename')
            })

    def cancel(self):
        self._is_cancelled = True
        self._pause_event.set()  # Unblock if paused to allow cancel exception

    def pause(self):
        self._pause_event.clear()

    def resume(self):
        self._pause_event.set()
