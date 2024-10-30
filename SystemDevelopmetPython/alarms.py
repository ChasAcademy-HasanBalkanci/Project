import json
from logger import logger
from email_notifier import EmailNotifier
# Create an AlarmManager class to handle alarms and notifications.
class AlarmManager:
    # Initialize the AlarmManager with an empty list of alarms and an email notifier.
    def __init__(self):
        self.alarms = {
            'CPU': [],
            'Memory': [],
            'Disk': []
        }
        self.email_notifier = EmailNotifier()
        self.alarm_file = 'configured_alarms.json' # File to store configured alarms.
        self.load_alarms()

    # allows the user to configure multiple alarms in one session before returning to the main menu, 
    # and ensures that all changes are saved when they're done configuring.
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
                self._set_alarm(choice) # setting of the alarm thresholds is handled in the _set_alarm method
            else:
                print("Invalid choice. Please try again.")
        self.save_alarms()

    '''This method allows users to set alarm thresholds for CPU, Memory, or Disk usage. 
    It includes input validation to ensure that only valid threshold values 
    (integers between 1 and 100) are accepted and stored.'''

    def _set_alarm(self, choice):
        alarm_types = {
            '1': 'CPU',
            '2': 'Memory',
            '3': 'Disk'
        }
        alarm_type = alarm_types[choice] # Get alarm type from choice
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
    # Show current alrms sorting by threshold
    def show_alarms(self):
        print("\n--- Current Alarms ---")
        for alarm_type, thresholds in self.alarms.items():
            if thresholds:
                print(f"{alarm_type}: {', '.join(map(str, sorted(thresholds)))}%") # Sort and join thresholds
            else:
                print(f"{alarm_type}: No alarms set")

    def remove_alarms(self):
        while True:
            print("\n--- Remove Alarms ---")
            all_alarms = []
            for alarm_type, thresholds in self.alarms.items():
                if thresholds:
                    print(f"\n--- {alarm_type} Alarm ---")
                    for threshold in sorted(thresholds):
                        index = len(all_alarms) + 1
                        print(f"{index}. {alarm_type} alarm {threshold}%")
                        all_alarms.append((alarm_type, threshold))
    
            if not all_alarms:
                print("No alarms configured.")
                return
    
            print(f"\n{len(all_alarms) + 1}. Back to Main Menu")
    
            try:
                choice = int(input("\nEnter your choice: "))
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
    # Check if any of the configured alarms have been triggered and send notifications if so.
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
    # allows the AlarmManager to persist alarm configurations between program runs.
    def load_alarms(self):
        try:
            with open(self.alarm_file, 'r') as f:
                self.alarms = json.load(f)
            print("Loading previously configured alarms...")
        except FileNotFoundError:
            print("No previously configured alarms found.")