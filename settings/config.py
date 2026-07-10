import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "download_dir": os.path.expanduser("~/Downloads/MediaYantra"),
    "concurrent_downloads": 3,
    "theme": "dark",
    "accent_color": "#A855F7",
    "cookies_browser": "None",
    "default_resolution": "Best Quality",
    "default_audio_format": "MP3",
    "embed_thumbnail": True,
    "embed_metadata": True,
    "embed_subtitles": False
}

class ConfigManager:
    def __init__(self):
        self.config = self.load_config()
        # Ensure default folder exists
        os.makedirs(self.config["download_dir"], exist_ok=True)

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            self.save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG
        
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                # Merge with defaults in case of new settings
                merged = DEFAULT_CONFIG.copy()
                merged.update(data)
                return merged
        except Exception:
            return DEFAULT_CONFIG

    def save_config(self, data=None):
        if data is None:
            data = self.config
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()

config = ConfigManager()
