class QueueManager:
    def __init__(self):
        self.queue = []
        self.active_downloads = {}
        
    def add_download(self, d_id, worker):
        self.queue.append(d_id)
        self.active_downloads[d_id] = worker
        worker.start()
        
    def cancel_download(self, d_id):
        if d_id in self.active_downloads:
            worker = self.active_downloads[d_id]
            worker.cancel()
            del self.active_downloads[d_id]

queue_manager = QueueManager()
