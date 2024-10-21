'''This is a Python function named display_menu that 
prints a menu to the console with 7 options for system monitoring.'''
def display_menu():
    print("System Monitoring Menu".center(50, "*"))
    print("\n1. Start Monitoring\n2. List Active Monitoring\n3. Create Alarm\n4. Show Alarms\n5. Start Watch Mode\n6. Remove Alarm\n7. Exit")
#display_menu()
def main():
    while True:
        try: 
            display_menu()
            choice = input("\nSelect an option (1-7): "))
            if choice == '7':
                print("Exiting the program...")
                break
            else:   
                if choice == '1':
                    start_monitoring()
                elif choice == '2':
                    list_active_monitoring()
                elif choice == '3':
                    create_alarm()
                elif choice == '4':
                    show_alarms()
                elif choice == '5':
                    start_watch_mode()
                elif choice == '6':
                    remove_alarm()

        except Exception as ex:
            print(f"Error: {ex}. You should try again." ) # print(ex), which shows the error
            

# def start_monitoring():
#     print("Monitoring started".center(50, "*"))  # Placeholder for actual monitoring logic

# def list_active_monitoring():
#     print("Listing active monitoring.".center(50, "*"))  # Placeholder for listing logic

# def create_alarm():
#     print("Creating an alarm".center(50, "*"  ))  # Placeholder for creating alarms

# def show_alarms():
#     print("Displaying alarms.".center(50, "*"))  # Placeholder for showing alarms

# def start_watch_mode():
#     print("Watch mode started.".center(50, "*"))  # Placeholder for watch mode logic

# def remove_alarm():
#     print("Removing alarm.".center(50, "*"))  # Placeholder for removing alarms

if __name__ == "__main__":
    main()


