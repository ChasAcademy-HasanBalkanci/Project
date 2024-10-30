import tkinter as tk
from tkinter import ttk
import threading
import time

class GUI:
    def __init__(self, system_monitor, alarm_manager):
        self.system_monitor = system_monitor
        self.alarm_manager = alarm_manager
        self.root = tk.Tk()
        self.root.title("System Monitor")
        self.root.geometry("400x300")
        self.setup_ui()

    def setup_ui(self):
        self.cpu_var = tk.StringVar()
        self.memory_var = tk.StringVar()
        self.disk_var = tk.StringVar()
        self.alarms_var = tk.StringVar()

        ttk.Label(self.root, text="System Status:").pack(pady=10)
        ttk.Label(self.root, textvariable=self.cpu_var).pack()
        ttk.Label(self.root, textvariable=self.memory_var).pack()
        ttk.Label(self.root, textvariable=self.disk_var).pack()

        ttk.Label(self.root, text="Active Alarms:").pack(pady=10)
        ttk.Label(self.root, textvariable=self.alarms_var).pack()

    def update_status(self):
        while True:
            status = self.system_monitor.get_current_status()
            self.cpu_var.set(f"CPU Usage: {status['CPU']}%")
            self.memory_var.set(f"Memory Usage: {status['Memory']}%")
            self.disk_var.set(f"Disk Usage: {status['Disk']}%")

            alarms = self.alarm_manager.check_alarms(status)
            alarm_text = "\n".join([f"{a['type']} alarm at {a['level']}%" for a in alarms]) or "No active alarms"
            self.alarms_var.set(alarm_text)

            time.sleep(3) # It can be arranged to update more frequently depending on the requirements

    def run(self):
        self.system_monitor.start_monitoring()
        threading.Thread(target=self.update_status, daemon=True).start()
        self.root.mainloop()
