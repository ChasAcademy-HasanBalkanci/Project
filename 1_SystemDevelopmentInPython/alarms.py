class Alarms:
    def __init__(self, alarms):
        self.alarms = alarms

    def configure_alarms(self):
        while True:
            print("\nConfigure alarms:")
            print("1. CPU usage")
            print("2. Memory usage")
            print("3. Disk usage")
            print("4. Back to main menu")

            choice = input("Select an option: ")

            if choice in ['1', '2', '3']:
                level = input("Set level for alarm (0-100): ")
                if level.isdigit() and 0 <= int(level) <= 100:
                    alarm_type = 'CPU' if choice == '1' else 'Memory' if choice == '2' else 'Disk'
                    self.alarms.append({'type': alarm_type, 'level': int(level)})
                    print(f"Alarm for {alarm_type} usage set to {level}%.")
                else:
                    print("Invalid level. Please enter a number between 0 and 100.")
            elif choice == '4':
                break
            else:
                print("Invalid option. Please try again.")

    def show_alarms(self):
        if not self.alarms:
            print("No alarms configured.")
            return
        sorted_alarms = sorted(self.alarms, key=lambda x: (x['type'], x['level']))
        for alarm in sorted_alarms:
            print(f"{alarm['type']} Alarm {alarm['level']}%")
        input("Press any key to return to the main menu.")

    def remove_alarm(self):
        if not self.alarms:
            print("No alarms to remove.")
            return
        for idx, alarm in enumerate(self.alarms):
            print(f"{idx + 1}. {alarm['type']} Alarm {alarm['level']}%")
        choice = input("Select an alarm to delete (number): ")
        if choice.isdigit() and 1 <= int(choice) <= len(self.alarms):
            removed_alarm = self.alarms.pop(int(choice) - 1)
            print(f"Removed {removed_alarm['type']} Alarm {removed_alarm['level']}%.")
        else:
            print("Invalid choice.")

    def get_alarms(self):
        return self.alarms
