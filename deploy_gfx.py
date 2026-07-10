import shutil
import os
import codecs

os.makedirs('assets', exist_ok=True)
shutil.copy(r'C:\Users\okoth\.gemini\antigravity\brain\1c053bba-d20b-4d64-bae1-f6ea7b886c04\dark_tech_bg_1783695301587.png', r'assets\bg.png')

replaces = {
    "ui/video_dl.py": ("🎬", "⯈"),
    "ui/playlist_dl.py": ("📑", "▤"),
    "ui/mp3_dl.py": ("🎵", "𝅘𝅥𝅯"),
    "ui/download_manager.py": ("💾", "⭳"),
    "ui/settings.py": ("⚙️", "⛭")
}

for path, (old, new) in replaces.items():
    if os.path.exists(path):
        with codecs.open(path, 'r', 'utf-8') as f:
            t = f.read()
        with codecs.open(path, 'w', 'utf-8') as f:
            f.write(t.replace(old, new))

# Modify spec carefully
if os.path.exists('Media_Yantra_Final.spec'):
    with codecs.open('Media_Yantra_Final.spec', 'r', 'utf-8') as f:
        spec = f.read()
    if "datas=[" in spec and "'assets'" not in spec:
        spec = spec.replace("datas=[", "datas=[('assets', 'assets'), ")
    with codecs.open('Media_Yantra_Final.spec', 'w', 'utf-8') as f:
        f.write(spec)
