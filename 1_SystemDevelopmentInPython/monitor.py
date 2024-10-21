import psutil
import json
from alarm import Alarm
from logger import Logger
from utils import input_with_validation

class Monitor:
    def __init__(self, logger):
        self.logger = logger
        self.alarms = []
        self.monitoring_active = False

    def load_alarms(self):
        try:
            with open('alarms.json', 'r') as f:
                self.alarms = [Alarm(**alarm) for alarm in json.load(f)]
                print("Loading previously configured alarms...")
        except FileNotFoundError:
            print("No previous alarms found.")

    def start_monitoring(self):
        if not self.monitoring_active:
            self.monitoring_active = True
            self.logger.log("Monitoring started.")
            print("Monitoring has been started.")
        else:
            print("Monitoring is already active.")

    def list_active_monitoring(self):
        if self.monitoring_active:
            cpu_usage = psutil.cpu_percent()
            memory_info = psutil.virtual_memory()
            disk_info = psutil.disk_usage('/')

            print(f"CPU Usage: {cpu_usage}%")
            print(f"Memory Usage: {memory_info.percent}% ({memory_info.used / (1024 ** 2):.2f} MB out of {memory_info.total / (1024 ** 2):.2f} MB used)")
            print(f"Disk Usage: {disk_info.percent}% ({disk_info.used / (1024 ** 3):.2f} GB out of {disk_info.total / (1024 ** 3):.2f} GB used)")
        else:
            print("No monitoring is active.")

    def create_alarm(self):
        print("Configure Alarm:")
        alarm_type = input("Choose alarm type (CPU, Memory, Disk): ").strip().lower()
        level = input_with_validation("Set alarm level between 0-100: ", 0, 100)
        
        alarm = Alarm(alarm_type, level)
        self.alarms.append(alarm)
        self.logger.log(f"Alarm for {alarm_type} set to {level}%.")
        print(f"Alarm for {alarm_type} set to {level}%.")
        self.save_alarms()

    def show_alarms(self):
        if self.alarms:
            for idx, alarm in enumerate(self.alarms, start=1):
                print(f"{idx}. {alarm}")
        else:
            print("No configured alarms.")

    def start_monitoring_mode(self):
        if self.monitoring_active:
            print("Monitoring mode is active. Press any key to return to the menu.")
            # Simulate monitoring mode...
        else:
            print("Monitoring must be started first.")

    def remove_alarm(self):
        self.show_alarms()
        if self.alarms:
            index = int(input("Choose a configured alarm to remove: ")) - 1
            if 0 <= index < len(self.alarms):
                removed_alarm = self.alarms.pop(index)
                self.logger.log(f"Alarm removed: {removed_alarm}")
                print(f"Alarm removed: {removed_alarm}")
                self.save_alarms()
            else:
                print("Invalid choice.")

    def save_alarms(self):
        with open('alarms.json', 'w') as f:
            json.dump([alarm.to_dict() for alarm in self.alarms], f)
