import sys
sys.path.insert(0, r"o:\media yantra")
from download.video_worker import DownloadWorker
from utils.logger_util import app_logger

app_logger.register_callback(lambda msg: print("LOG:", msg))

url = "https://youtu.be/Xi6BjmipH58?si=eV014219zHj_G4wl"
opts = {
    'outtmpl': r"o:\media yantra\%(title)s.%(ext)s",
    'format': 'bestvideo[height<=144]+bestaudio/best',
    'merge_output_format': 'mp4'
}

def on_prog(d): print("PROG", d.get('status'))
def on_fini(i): print("FINI")
def on_err(e): print("ERR", e)

worker = DownloadWorker(url, opts, on_prog, on_fini, on_err)
worker.start()
worker.join()
