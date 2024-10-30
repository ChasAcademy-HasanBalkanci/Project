import os
from datetime import datetime # Importing datetime module for timestamping
# Create a Logger class to handle logging messages.
class Logger:
    def __init__(self):
        self.log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = self._create_log_file()

    def _create_log_file(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.log_dir, f"log_{timestamp}.txt")

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        with open(self.log_file, 'a') as f:
            f.write(formatted_message)

logger = Logger()