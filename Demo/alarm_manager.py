import json
from functools import reduce

class AlarmManager:
    def __init__(self):
        self.alarms = {
            'CPU': [],
            'Memory': [],
            'Disk': []
        }

    def create_alarms(self):
        while True:
            print("\nConfigure alarms:")
            print("1. CPU usage")
            print("2. Memory usage")
            print("3. Disk usage")
            print("4. Back to main menu")

            choice = input("Enter your choice (1-4): ")

            if choice == '4':
                break

            if choice in ['1', '2', '3']:
                alarm_type = ['CPU', 'Memory', 'Disk'][int(choice) - 1]
                level = input("Set level for alarm between 0-100: ")
                try:
                    level = int(level)
                    if 0 <= level <= 100:
                        if alarm_type not in self.alarms:
                            self.alarms[alarm_type] = []
                        self.alarms[alarm_type].append(level)
                        print(f"Alarm for {alarm_type} usage set to {level}%.")
                        self.save_alarms()
                    else:
                        print("Error: Level must be between 0 and 100.")
                except ValueError:
                    print("Error: Please enter a valid number.")
            else:
                print("Invalid choice. Please try again.")

    def show_alarms(self):
        print("Configured alarms:".center(50, "*"))
        for alarm_type, levels in self.alarms.items():
            for level in sorted(levels, reverse=True):
                print(f"{alarm_type} alarm {level}%")

    # Check if any alarms are triggered
    def check_alarms(self, status):
        triggered_alarms = []
        for alarm_type, levels in self.alarms.items():
            if levels:
                triggered_levels = [level for level in levels if status[alarm_type] >= level]
                if triggered_levels:
                    # Reduce the list of triggered levels to the maximum value.
                    triggered_alarms.append({'type': alarm_type, 'level': max(triggered_levels)})
        return sorted(triggered_alarms, key=lambda x: x['level'], reverse=True)

    def remove_alarms(self):
        self.show_alarms()
        print("\nSelect a configured alarm to delete:")
        all_alarms = [(t, l) for t in self.alarms for l in self.alarms[t]]
        
        for i, (alarm_type, level) in enumerate(all_alarms, 1):
            print(f"{i}. {alarm_type} alarm {level}%")
        
        choice = input("Enter the number of the alarm to delete (or Enter to cancel): ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(all_alarms):
                alarm_type, level = all_alarms[choice - 1]
                self.alarms[alarm_type].remove(level)
                print(f"Alarm for {alarm_type} usage at {level}% has been removed.")
                self.save_alarms()
            elif choice != 0:
                print("Invalid choice. No alarm removed.")
        except ValueError:
            print("Invalid input. No alarm removed.")

    def save_alarms(self):
        with open('alarms.json', 'w') as f:
            json.dump(self.alarms, f)
    
    def load_alarms(self):
        try:
            with open('alarms.json', 'r') as f:
                loaded_data = json.load(f)
                if isinstance(loaded_data, dict):
                    # Ensure the loaded data has the correct structure
                    for key in ['CPU', 'Memory', 'Disk']:
                        if key not in loaded_data or not isinstance(loaded_data[key], list):
                            loaded_data[key] = []
                    self.alarms = loaded_data
                else:
                    # If loaded_data is not a dictionary, initialize with empty lists
                    self.alarms = {'CPU': [], 'Memory': [], 'Disk': []}
                print("Loading previously configured alarms...")
        except FileNotFoundError:
            print("No previously configured alarms found.")
            self.alarms = {'CPU': [], 'Memory': [], 'Disk': []}
        except json.JSONDecodeError:
            print("Error reading alarms file. Starting with empty alarms.")
            self.alarms = {'CPU': [], 'Memory': [], 'Disk': []}


    

