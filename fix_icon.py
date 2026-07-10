import codecs
import os

def replace_in_file(path, old, new):
    if not os.path.exists(path):
        return
    with codecs.open(path, 'r', 'utf-8') as f:
        content = f.read()
    with codecs.open(path, 'w', 'utf-8') as f:
        f.write(content.replace(old, new))

replace_in_file("ui/app.py", "app_icon.ico", "icon.ico")
replace_in_file("Media_Yantra_Final.spec", "app_icon.ico", "icon.ico")
replace_in_file("setup.iss", "app_icon.ico", "icon.ico")
