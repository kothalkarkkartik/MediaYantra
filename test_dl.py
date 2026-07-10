import sys
sys.path.insert(0, r"o:\media yantra")
from download.video_worker import DownloadWorker

def on_prog(d):
    print(f"PROGRESS UPDATE: {d}")
    
def on_fini(info):
    print("FINISH UPDATE")
    
def on_err(err):
    print(f"ERROR UPDATE: {err}")

opts = {
    'outtmpl': r"o:\media yantra\%(title)s.%(ext)s",
    'format': 'bestvideo[height<=360]+bestaudio/best',
    'merge_output_format': 'mp4'
}

worker = DownloadWorker("https://www.youtube.com/watch?v=jNQXAC9IVRw", opts, on_prog, on_fini, on_err)
worker.start()
worker.join()
