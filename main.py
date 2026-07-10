import sys
import os

# Important for PyInstaller bundle context
if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, application_path)

from ui.app import MediaYantraApp

if __name__ == "__main__":
    app = MediaYantraApp()
    app.mainloop()
