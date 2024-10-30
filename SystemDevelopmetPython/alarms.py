import json
from logger import logger
from email_notifier import EmailNotifier

class AlarmManager:
    def __init__(self):
        self.alarms = {
            'CPU': [],
            'Memory': [],
            'Disk': []
        }
        self.email_notifier = EmailNotifier()
        self.alarm_file = 'configured_alarms.json'
        self.load_alarms()

    def configure_alarms(self):
        while True:
            print("\n--- Configure Alarms ---")
            print("1. CPU Usage")
            print("2. Memory Usage")
            print("3. Disk Usage")
            print("4. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == '4':
                break
            elif choice in ['1', '2', '3']:
                self._set_alarm(choice)
            else:
                print("Invalid choice. Please try again.")
        self.save_alarms()

    def _set_alarm(self, choice):
        alarm_types = {
            '1': 'CPU',
            '2': 'Memory',
            '3': 'Disk'
        }
        alarm_type = alarm_types[choice]
        threshold = input(f"Enter {alarm_type} usage threshold (1-100): ")
        try:
            threshold = int(threshold)
            if 1 <= threshold <= 100:
                self.alarms[alarm_type].append(threshold)
                print(f"{alarm_type} alarm set at {threshold}%")
                logger.log(f"Alarm_Set_{alarm_type}_{threshold}")
            else:
                print("Invalid threshold. Please enter a number between 1 and 100.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def show_alarms(self):
        print("\n--- Current Alarms ---")
        for alarm_type, thresholds in self.alarms.items():
            if thresholds:
                print(f"{alarm_type}: {', '.join(map(str, thresholds))}%")
            else:
                print(f"{alarm_type}: No alarms set")

    def remove_alarms(self):
        while True:
            print("\n--- Remove Alarms ---")
            all_alarms = []
            for alarm_type, thresholds in self.alarms.items():
                for threshold in thresholds:
                    all_alarms.append((alarm_type, threshold))

            if not all_alarms:
                print("No alarms configured.")
                return

            print("Select a configured alarm to delete:")
            for i, (alarm_type, threshold) in enumerate(all_alarms, 1):
                print(f"{i}. {alarm_type} alarm {threshold}%")
            print(f"{len(all_alarms) + 1}. Back to Main Menu")

            try:
                choice = int(input("Enter your choice: "))
                if choice == len(all_alarms) + 1:
                    break
                elif 1 <= choice <= len(all_alarms):
                    alarm_type, threshold = all_alarms[choice - 1]
                    self.alarms[alarm_type].remove(threshold)
                    print(f"{alarm_type} alarm at {threshold}% removed")
                    logger.log(f"Alarm_Removed_{alarm_type}_{threshold}")
                    self.save_alarms()
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def check_alarms(self, cpu_percent, memory_percent, disk_percent):
        triggered_alarms = []
        if any(cpu_percent > threshold for threshold in self.alarms['CPU']):
            triggered_alarms.append(f"CPU usage ({cpu_percent:.1f}%) exceeds threshold")
        if any(memory_percent > threshold for threshold in self.alarms['Memory']):
            triggered_alarms.append(f"Memory usage ({memory_percent:.1f}%) exceeds threshold")
        if any(disk_percent > threshold for threshold in self.alarms['Disk']):
            triggered_alarms.append(f"Disk usage ({disk_percent:.1f}%) exceeds threshold")

        if triggered_alarms:
            alarm_message = "\n".join(triggered_alarms)
            print("\nALARM: " + alarm_message)
            logger.log("Alarm_Triggered")
            self.email_notifier.send_notification("System Monitor Alarm", alarm_message)

    def save_alarms(self):
        with open(self.alarm_file, 'w') as f:
            json.dump(self.alarms, f)

    def load_alarms(self):
        try:
            with open(self.alarm_file, 'r') as f:
                self.alarms = json.load(f)
            print("Loading previously configured alarms...")
        except FileNotFoundError:
            print("No previously configured alarms found.")