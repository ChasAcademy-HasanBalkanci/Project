import json
import os
from monitor import Monitor
from alarms import Alarms
from email_service import EmailService
from logger import Logger
from gui import MonitoringApp
import tkinter as tk

def load_alarms(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return []

def main():
    logger = Logger("monitoring_log.txt")
    email_service = EmailService()
    alarms = Alarms(load_alarms("alarms.json"))
    monitor = Monitor(alarms, email_service)

    # Start GUI
    root = tk.Tk()
    app = MonitoringApp(root)
    root.mainloop()


    while True:
        print("\n1. Start Monitoring")
        print("2. List Active Monitoring")
        print("3. Create Alarms")
        print("4. Show Alarms")
        print("5. Start Monitoring Mode")
        print("6. Remove Alarm")
        print("7. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            monitor.start_monitoring()
        elif choice == "2":
            monitor.list_active_monitoring()
        elif choice == "3":
            alarms.configure_alarms()
        elif choice == "4":
            alarms.show_alarms()
        elif choice == "5":
            monitor.start_monitoring_mode()
        elif choice == "6":
            alarms.remove_alarm()
        elif choice == "7":
            with open("alarms.json", 'w') as f:
                json.dump(alarms.get_alarms(), f)
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
