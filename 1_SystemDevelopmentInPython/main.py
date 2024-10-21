from monitor import Monitor
from logger import Logger

def main():
    logger = Logger('monitoring_log.txt')
    monitor = Monitor(logger)

    # Load previously configured alarms
    monitor.load_alarms()

    while True:
        print("\n--- Main Menu ---")
        print("1. Start Monitoring")
        print("2. List Active Monitoring")
        print("3. Create Alarm")
        print("4. Show Alarms")
        print("5. Start Monitoring Mode")
        print("6. Remove Alarm")
        print("7. Exit")

        choice = input("Choose an option: ")
        if choice == '1':
            monitor.start_monitoring()
        elif choice == '2':
            monitor.list_active_monitoring()
        elif choice == '3':
            monitor.create_alarm()
        elif choice == '4':
            monitor.show_alarms()
        elif choice == '5':
            monitor.start_monitoring_mode()
        elif choice == '6':
            monitor.remove_alarm()
        elif choice == '7':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
