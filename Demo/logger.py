from datetime import datetime
import os

class Logger:
    def __init__(self):
        self.log_dir = "logs"
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        self.log_file = os.path.join(self.log_dir, f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

    def log(self, message):
        timestamp = datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
        log_entry = f"{timestamp}_{message}\n"
        with open(self.log_file, "a") as f:
            f.write(log_entry)
