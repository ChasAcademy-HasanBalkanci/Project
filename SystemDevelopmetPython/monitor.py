import psutil
import time
import threading
import sys
import os
from logger import logger

class Monitor:
    def __init__(self):
        self.monitoring_active = False
        self.monitoring_thread = None

    def start_monitoring(self):
        self.monitoring_active = True
        logger.log("Monitoring_Started")
        print("Monitoring started.")

    def list_active_monitoring(self):
        if not self.monitoring_active:
            print("No active monitoring sessions.")
            logger.log("No_Active_Monitoring_Sessions")
            return

        cpu_usage = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        print(f"CPU Usage: {cpu_usage:.1f}%")
        print(f"Memory Usage: {memory.percent:.1f}% ({memory.used / (1024**3):.1f} GB out of {memory.total / (1024**3):.1f} GB used)")
        print(f"Disk Usage: {disk.percent:.1f}%")

    def monitor_system(self, alarm_manager):
        while self.monitoring_active:
            cpu_usage = psutil.cpu_percent()
            memory_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent

            print(f"\rCPU: {cpu_usage:.1f}% | Memory: {memory_usage:.1f}% | Disk: {disk_usage:.1f}%", end="")
            sys.stdout.flush()

            alarm_manager.check_alarms(cpu_usage, memory_usage, disk_usage)
            time.sleep(1)

    def start_monitoring_mode(self, alarm_manager):
        self.monitoring_active = True
        logger.log("Monitoring_Mode_Started")
        print("Starting monitoring mode...")
        print("Press 'q' to quit or Ctrl+C to interrupt.")

        self.monitoring_thread = threading.Thread(target=self.monitor_system, args=(alarm_manager,))
        self.monitoring_thread.start()

        try:
            while self.monitoring_active:
                if sys.stdin.isatty():
                    if os.name == 'nt':  # Windows
                        import msvcrt
                        if msvcrt.kbhit():
                            if msvcrt.getch().decode().lower() == 'q':
                                break
                    else:  # Unix-like systems
                        import select
                        if select.select([sys.stdin], [], [], 0.1)[0]:
                            if sys.stdin.read(1).lower() == 'q':
                                break
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_monitoring()

    def stop_monitoring(self):
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join()
        print("\nMonitoring stopped.")
        logger.log("Monitoring_Stopped")