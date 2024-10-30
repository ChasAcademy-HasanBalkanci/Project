# Import necessary modules and classes
import os
from menu import display_menu
from monitor import Monitor
from alarms import AlarmManager
from logger import logger
from gui import MonitoringGUI

# Function to check if email setup is complete
def check_email_setup():
    required_vars = ['SENDGRID_API_KEY', 'FROM_EMAIL', 'TO_EMAIL'] 
    missing_vars = [var for var in required_vars if not os.environ.get(var)] # Check if all required environment variables are set
    
    # Log missing environment variables if any
    if missing_vars:
        print("Warning: Email notification setup is incomplete.")
        print("Please set the following environment variables:")
        for var in missing_vars:
            print(f"- {var}")
        print("Email notifications will be disabled until these are set.")
        logger.log("Email_Notification_Setup_Incomplete")

# Main function to run the application
def main():
    # Check email setup before starting the application
    check_email_setup()
    
    # Initialize key components of the application
    monitor = Monitor()
    alarm_manager = AlarmManager()
    gui = MonitoringGUI(alarm_manager) # Initialize GUI with alarm manager for mode monitoring
    
    # Log application start
    logger.log("Application_Started")
    
    # Main application loop
    while True:
        # Display menu and get user choice
        choice = display_menu() 
        logger.log(f"User_Input_{choice}")
        
        # Handle user choices
        if choice == '1':
            monitor.start_monitoring()
        elif choice == '2':
            monitor.list_active_monitoring()
        elif choice == '3':
            alarm_manager.configure_alarms()
        elif choice == '4':
            alarm_manager.show_alarms()
        elif choice == '5':
            alarm_manager.remove_alarms()
        elif choice == '6':
            monitor.start_monitoring_mode(alarm_manager)
        elif choice == '7':
            print("Running GUI. Close the GUI window to return to the main menu.")
            gui.run()
            gui.stop()  # Ensure the GUI is properly stopped before continuing
            
        elif choice.lower() == '8':
            # Exit the application
            logger.log("Application_Exited")
            print("Exiting the application. Goodbye!")
            break # Exit the loop
        else:
            # Handle invalid input
            print("Invalid choice. Please try again.")
            logger.log("Invalid_Menu_Choice")

# Entry point of the script
if __name__ == "__main__":
    main()