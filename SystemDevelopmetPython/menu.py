# Creates and displays a menu for a System Monitoring Application.
def display_menu():
    menu_options = [
        "Start Monitoring",
        "List Active Monitoring",
        "Configure Alarms",
        "Show Alarms",
        "Remove Alarms",
        "Start Monitoring Mode",
        "Launch GUI",
        "Quit"
    ]
    
    print("\n--- System Monitoring Application ---")
    for i, option in enumerate(menu_options, 1):
        print(f"{i}. {option}")
    
    while True:
        choice = input("Enter your choice: ")
        if choice.lower() == 'q':
            return 'q'
        elif choice.isdigit() and 1 <= int(choice) <= len(menu_options):
            return choice
        else:
            print("Invalid choice. Please try again.")