import os
import threading
import time
from system_monitor import SystemMonitor
from alarm_manager import AlarmManager
from logger import Logger
from utils import clear_screen, key_pressed
from gui import GUI
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config import SENDGRID_API_KEY, EMAIL_FROM, EMAIL_TO

class MonitoringApp:
    def __init__(self):
        self.system_monitor = SystemMonitor()
        self.alarm_manager = AlarmManager()
        self.logger = Logger()
        self.gui = GUI(self.system_monitor, self.alarm_manager)
        self.stop_monitoring = threading.Event()  # Event to stop the monitoring loop


    def run(self):
        self.logger.log("Application started")
        self.alarm_manager.load_alarms()
        
        while True:
            clear_screen() # Clear the screen before displaying the menu. calls from utils.py
            print("Monitoring Application".center(50, "*"))
            print("\n1. Start monitoring")
            print("2. List active monitoring")
            print("3. Create alarms")
            print("4. Show alarms")
            print("5. Start monitoring mode")
            print("6. Remove alarms")
            print("7. Start GUI")
            print("8. Exit")

            choice = input("\nEnter your choice (1-8): ")
            self.logger.log(f"User selected option: {choice}")

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
                self.remove_alarms()
            elif choice == '7':
                self.start_gui()
            elif choice == '8':
                self.logger.log("Application exited")
                print("Exiting the application. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def start_monitoring(self):
        self.system_monitor.start_monitoring()
        self.logger.log("Monitoring started")
        print("Monitoring started.")
        input("\nPress Enter to return to the main menu: ")

    def list_active_monitoring(self):
        if not self.system_monitor.is_monitoring_active():
            print("No monitoring is active.")
            input("\nPress Enter to return to the main menu: ")
        else:
            print("Active monitoring:".center(50, "*"))
            self.system_monitor.print_current_status()
            self.logger.log("Active monitoring listed")
            input("\nPress Enter to return to the main menu: ") # Wait for the user to press Enter to return to the main menu. Calls from utils.py
    def create_alarms(self):
        self.alarm_manager.create_alarms()
        self.logger.log("Alarms created")

    def show_alarms(self):
        self.alarm_manager.show_alarms()
        self.logger.log("Alarms displayed")
        input("\nPress Enter to return to the main menu: ")

    def start_monitoring_mode(self):
        self.logger.log("Monitoring mode started")
        # Start the thread to handle user input (pressing Enter)
        input_thread = threading.Thread(target=self.wait_for_enter)
        input_thread.daemon = True  # Ensures thread exits when the main program does
        input_thread.start()  
        
        while not self.stop_monitoring.is_set():  # Run until stop event is set
            if not self.system_monitor.is_monitoring_active():
                print("Monitoring is not active. Please start monitoring first.")
                input("\nPress Enter to return to the main menu: ")
                break
            status = self.system_monitor.get_current_status()
            triggered_alarms = self.alarm_manager.check_alarms(status)
            print("Monitoring mode started.".center(50, "*"))
            for alarm in triggered_alarms:
                print(f"***WARNING, ALARM ENABLED, {alarm['type']} USAGE EXCEEDS {alarm['level']}%***\n")
                self.logger.log(f"{alarm['type']} alarm activated at {alarm['level']}%")
                self.send_email_alert(alarm)
            time.sleep(5)
            self.logger.log("Monitoring mode stopped")
            print("Returning to the main menu.")
                   
    def wait_for_enter(self):
        input()  # Wait for the user to press Enter
        self.stop_monitoring.set()  # Set the event to stop the monitoring loop
    def remove_alarms(self):
        self.alarm_manager.remove_alarms()
        self.logger.log("Alarm removed")

    def start_gui(self):
        self.gui.run()

    def send_email_alert(self, alarm):
        message = Mail(
            from_email=EMAIL_FROM,
            to_emails=EMAIL_TO,
            subject='System Monitoring Alarm',
            html_content=f'<strong>{alarm["type"]} usage exceeded {alarm["level"]}%</strong>')
        try:
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
            self.logger.log(f"Email alert sent for {alarm['type']} alarm")
        except Exception as e:
            self.logger.log(f"Error sending email alert: {str(e)}")
