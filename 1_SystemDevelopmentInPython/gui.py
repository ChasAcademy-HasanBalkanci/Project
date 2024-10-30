import tkinter as tk
from tkinter import messagebox
from monitor import Monitor
from alarms import Alarms
from email_service import EmailService

class MonitoringApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Monitoring Application")

        self.alarms = Alarms([])
        self.email_service = EmailService()
        self.monitor = Monitor(self.alarms, self.email_service)

        self.active_alarms_frame = tk.Frame(master)
        self.active_alarms_frame.pack(pady=10)

        self.label = tk.Label(self.active_alarms_frame, text="Active Alarms", font=("Arial", 16))
        self.label.pack()

        self.alarms_listbox = tk.Listbox(self.active_alarms_frame, width=50, height=10)
        self.alarms_listbox.pack()

        self.start_button = tk.Button(master, text="Start Monitoring", command=self.start_monitoring)
        self.start_button.pack(pady=5)

        self.quit_button = tk.Button(master, text="Quit", command=master.quit)
        self.quit_button.pack(pady=5)

        self.update_alarms()

    def start_monitoring(self):
        self.monitor.start_monitoring()
        self.update_alarms()

    def update_alarms(self):
        self.alarms_listbox.delete(0, tk.END)
        for alarm in self.alarms.get_alarms():
            self.alarms_listbox.insert(tk.END, f"{alarm['type']} Alarm: {alarm['level']}%")
        self.master.after(5000, self.update_alarms)  # Update every 5 seconds

if __name__ == "__main__":
    root = tk.Tk()
    app = MonitoringApp(root)
    root.mainloop()
