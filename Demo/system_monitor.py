import psutil

class SystemMonitor:
    def __init__(self):
        self.monitoring_active = False

    def start_monitoring(self):
        self.monitoring_active = True
       
    def is_monitoring_active(self):
        return self.monitoring_active

    def get_current_status(self):
        cpu_usage = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        return {
            'CPU': cpu_usage,
            'Memory': memory.percent,
            'Disk': disk.percent
        }

    def print_current_status(self):
        status = self.get_current_status()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        print(f"CPU Usage: {status['CPU']}%")
        print(f"Memory usage: {status['Memory']}% ({memory.used / (1024**3):.1f} GB out of {memory.total / (1024**3):.1f} GB used)")
        print(f"Disk usage: {status['Disk']}% ({disk.used / (1024**3):.1f} GB out of {disk.total / (1024**3):.1f} GB used)")
