import os
import codecs
from PIL import Image

src_img = r'C:\Users\okoth\.gemini\antigravity\brain\1c053bba-d20b-4d64-bae1-f6ea7b886c04\app_logo_1783696620394.png'
ico_path = r'assets/app_icon.ico'

# Make .ico
img = Image.open(src_img)
img.save(ico_path, format='ICO', sizes=[(256, 256)])

# Patch ui/app.py
with codecs.open('ui/app.py', 'r', 'utf-8') as f:
    code = f.read()
if 'self.iconbitmap' not in code:
    find = 'self.title("Media Yantra")'
    replace = '''self.title("Media Yantra")
        def resource_path(relative_path):
            import sys, os
            try: return os.path.join(sys._MEIPASS, relative_path)
            except Exception: return os.path.join(os.path.abspath("."), relative_path)
        try: self.iconbitmap(resource_path(os.path.join("assets", "app_icon.ico")))
        except Exception as e: print("Icon Error:", e)'''
    code = code.replace(find, replace)
    with codecs.open('ui/app.py', 'w', 'utf-8') as f:
        f.write(code)

# Patch PyInstaller spec
with codecs.open('Media_Yantra_Final.spec', 'r', 'utf-8') as f:
    spec = f.read()

if 'icon=' not in spec:
    find = 'console=False,'
    replace = 'console=False, icon="assets/app_icon.ico",'
    spec = spec.replace(find, replace)
    with codecs.open('Media_Yantra_Final.spec', 'w', 'utf-8') as f:
        f.write(spec)
