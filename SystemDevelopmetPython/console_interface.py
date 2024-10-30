import time
import sys
import select
import os

class ConsoleInterface:
    def __init__(self, monitor, alarm_system, logger, email_notifier):
        self.monitor = monitor
        self.alarm_system = alarm_system
        self.logger = logger
        self.email_notifier = email_notifier

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            self.logger.log(f"User input: {choice}")

            if choice == '1':
                self.start_monitoring()
            elif choice == '2':
                self.list_active_monitoring()
            elif choice == '3':
                self.create_alarms()
            elif choice == '4':
                self.show_alarms()
            elif choice == '5':
                self.start_monitoring_mode()
            elif choice == '6':
                self.remove_alarm()
            elif choice == '7':
                self.logger.log("Program exited")
                break
            else:
                print("Invalid choice. Please try again.")

    def display_menu(self):
        print("\n--- System Monitor Menu ---")
        print("1. Start monitoring")
        print("2. List active monitoring")
        print("3. Create alarms")
        print("4. Show alarms")
        print("5. Start monitoring mode")
        print("6. Remove alarm")
        print("7. Exit")

    def start_monitoring(self):
        self.monitor.start_monitoring()
        print("Monitoring started.")

    def list_active_monitoring(self):
        if not self.monitor.is_monitoring:
            print("No monitoring is active.")
        else:
            data = self.monitor.get_current_data()
            print(f"CPU Usage: {data['cpu']}%")
            print(f"Memory usage: {data['memory']['percent']}% ({data['memory']['used'] / (1024**3):.1f} GB out of {data['memory']['total'] / (1024**3):.1f} GB used)")
            print(f"Disk usage: {data['disk']['percent']}% ({data['disk']['used'] / (1024**3):.1f} GB out of {data['disk']['total'] / (1024**3):.1f} GB used)")
        input("Press Enter to return to the main menu...")

    def create_alarms(self):
        print("\n--- Create Alarms ---")
        print("1. CPU usage")
        print("2. Memory usage")
        print("3. Disk usage")
        print("4. Back to main menu")

        choice = input("Enter your choice: ")
        if choice in ['1', '2', '3']:
            alarm_types = ['cpu', 'memory', 'disk']
            alarm_type = alarm_types[int(choice) - 1]
            threshold = input("Set level for alarm between 0-100: ")
            try:
                threshold = int(threshold)
                if 0 <= threshold <= 100:
                    if self.alarm_system.add_alarm(alarm_type, threshold):
                        print(f"Alarm for {alarm_type} usage set to {threshold}%")
                    else:
                        print("Failed to set alarm. Please try again.")
                else:
                    print("Invalid threshold. Please enter a number between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter a number between 0 and 100.")

    def show_alarms(self):
        alarms = self.alarm_system.get_alarms()
        for alarm_type, thresholds in alarms.items():
            for threshold in thresholds:
                print(f"{alarm_type.capitalize()} alarm {threshold}%")
        input("Press Enter to return to the main menu...")

    def start_monitoring_mode(self):
        print("Monitoring mode started. Press Enter to return to the main menu.")
        self.monitor.start_monitoring()
        while True:
            print("Monitoring is active, press Enter to return to the menu.")
            data = self.monitor.get_current_data()
            triggered_alarms = self.alarm_system.check_alarms(data)
            for alarm in triggered_alarms:
                print(f"***WARNING, ALARM ENABLED, {alarm}***")
                self.email_notifier.send_alarm_email(alarm)
            if self._check_for_input():
                break
        self.monitor.stop_monitoring()

    def remove_alarm(self):
        alarms = self.alarm_system.get_alarms()
        print("\n--- Remove Alarms ---")
        alarm_list = []
        for alarm_type, thresholds in alarms.items():
            for threshold in thresholds:
                alarm_list.append((alarm_type, threshold))
                print(f"{len(alarm_list)}. {alarm_type.capitalize()} alarm {threshold}%")
        print(f"{len(alarm_list) + 1}. Back to main menu")

        choice = input("Enter the number of the alarm to remove: ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(alarm_list):
                alarm_type, threshold = alarm_list[choice - 1]
                if self.alarm_system.remove_alarm(alarm_type, threshold):
                    print(f"Alarm removed: {alarm_type.capitalize()} alarm {threshold}%")
                else:
                    print("Failed to remove alarm. Please try again.")
            elif choice == len(alarm_list) + 1:
                return
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def _check_for_input(self):
        if os.name == 'nt':  # For Windows
            import msvcrt
            return msvcrt.kbhit()
        else:  # For Unix
            return select.select([sys.stdin], [], [], 0.1)[0]