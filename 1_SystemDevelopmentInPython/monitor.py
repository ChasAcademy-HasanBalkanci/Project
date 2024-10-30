import psutil
import time

class Monitor:
    def __init__(self, alarms, email_service):
        self.alarms = alarms
        self.email_service = email_service
        self.active = False

    def start_monitoring(self):
        self.active = True
        print("Monitoring started.")

    def list_active_monitoring(self):
        if not self.active:
            print("No monitoring is active.")
            return
        cpu_usage = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage('/')

        print(f"CPU Usage: {cpu_usage}%")
        print(f"Memory Usage: {memory_info.percent}% ({memory_info.used / (1024 ** 3):.2f} GB out of {memory_info.total / (1024 ** 3):.2f} GB used)")
        print(f"Disk Usage: {disk_info.percent}% ({disk_info.used / (1024 ** 3):.2f} GB out of {disk_info.total / (1024 ** 3):.2f} GB used)")

    def start_monitoring_mode(self):
        print("Monitoring mode has been started.")
        while self.active:
            time.sleep(5)
            cpu_usage = psutil.cpu_percent()
            memory_info = psutil.virtual_memory()
            disk_info = psutil.disk_usage('/')

            if self.check_alarms(cpu_usage, memory_info.percent, disk_info.percent):
                print("Monitoring is active, press any key to return to the menu.")

    def check_alarms(self, cpu_usage, memory_usage, disk_usage):
        triggered = False
        for alarm in self.alarms.get_alarms():
            if alarm['type'] == 'CPU' and cpu_usage > alarm['level']:
                message = f"***WARNING, ALARM ENABLED: CPU usage exceeds {alarm['level']}%***"
                print(message)
                self.email_service.send_email("CPU Alarm Triggered", message)
                triggered = True
            elif alarm['type'] == 'Memory' and memory_usage > alarm['level']:
                message = f"***WARNING, ALARM ENABLED: Memory usage exceeds {alarm['level']}%***"
                print(message)
                self.email_service.send_email("Memory Alarm Triggered", message)
                triggered = True
            elif alarm['type'] == 'Disk' and disk_usage > alarm['level']:
                message = f"***WARNING, ALARM ENABLED: Disk usage exceeds {alarm['level']}%***"
                print(message)
                self.email_service.send_email("Disk Alarm Triggered", message)
                triggered = True
        return triggered
