import datetime

class AppLogger:
    def __init__(self):
        self.logs = []
        self.callbacks = []
        
    def _add_log(self, level, msg):
        time_str = datetime.datetime.now().strftime("%H:%M:%S")
        entry = f"[{time_str}] {level}: {msg}"
        self.logs.insert(0, entry)
        if len(self.logs) > 200:
            self.logs.pop()
        
        # Explicit Physical Disk Logging
        try:
            with open("yantra_logs.txt", "a", encoding="utf-8") as rf:
                rf.write(entry + "\n")
        except:
            pass
            
        for cb in self.callbacks:
            cb(entry)
            
    def debug(self, msg):
        self._add_log("DEBUG", msg)
        
    def warning(self, msg):
        self._add_log("WARNING", msg)
        
    def error(self, msg):
        self._add_log("ERROR", msg)
        
    def clear(self):
        self.logs = []
        try:
            with open("yantra_logs.txt", "w", encoding="utf-8") as rf:
                rf.write("")
        except:
            pass
        
    def register_callback(self, cb):
        self.callbacks.append(cb)

app_logger = AppLogger()
