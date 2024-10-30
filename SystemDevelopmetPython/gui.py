import tkinter as tk
from tkinter import ttk
import threading
import time
import psutil

class MonitoringGUI:
    def __init__(self, alarm_manager):
        self.alarm_manager = alarm_manager
        self.running = False
        self.root = None
        self.update_thread = None

    def create_gui(self):
        try:
            # Attempt to get the existing Tk instance
            self.root = tk.Tk()
            self.root.withdraw()  # Hide the root window
            self.root = tk.Toplevel()  # Create a new top-level window
        except tk.TclError:
            # If no Tk instance exists, create a new one
            self.root = tk.Tk()
        
        self.root.title("System Monitoring")
        self.root.geometry("600x400")
        self.create_widgets()
    def create_widgets(self):
        # Usage Frames
        usage_frame = ttk.LabelFrame(self.root, text="System Usage")
        usage_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.cpu_progress = ttk.Progressbar(usage_frame, length=200, mode='determinate')
        self.cpu_progress.grid(row=0, column=0, padx=5, pady=5)
        self.cpu_label = ttk.Label(usage_frame, text="CPU: 0%")
        self.cpu_label.grid(row=0, column=1, padx=5, pady=5)

        self.memory_progress = ttk.Progressbar(usage_frame, length=200, mode='determinate')
        self.memory_progress.grid(row=1, column=0, padx=5, pady=5)
        self.memory_label = ttk.Label(usage_frame, text="Memory: 0%")
        self.memory_label.grid(row=1, column=1, padx=5, pady=5)

        self.disk_progress = ttk.Progressbar(usage_frame, length=200, mode='determinate')
        self.disk_progress.grid(row=2, column=0, padx=5, pady=5)
        self.disk_label = ttk.Label(usage_frame, text="Disk: 0%")
        self.disk_label.grid(row=2, column=1, padx=5, pady=5)

        # Alarms Frame
        alarms_frame = ttk.LabelFrame(self.root, text="Active Alarms")
        alarms_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.alarms_text = tk.Text(alarms_frame, height=10, width=70)
        self.alarms_text.pack(padx=5, pady=5)

    def update_values(self):
        while self.running:
            cpu_percent = psutil.cpu_percent()
            memory_percent = psutil.virtual_memory().percent
            disk_percent = psutil.disk_usage('/').percent

            if self.root and self.root.winfo_exists():
                try:
                    self.root.after(0, self.update_gui, cpu_percent, memory_percent, disk_percent)
                    self.root.after(0, self.check_alarms, cpu_percent, memory_percent, disk_percent)
                except tk.TclError:
                    break
            else:
                break

            time.sleep(2)
    def update_gui(self, cpu_percent, memory_percent, disk_percent):
        self.cpu_progress['value'] = cpu_percent
        self.cpu_label['text'] = f"CPU: {cpu_percent:.1f}%"

        self.memory_progress['value'] = memory_percent
        self.memory_label['text'] = f"Memory: {memory_percent:.1f}%"

        self.disk_progress['value'] = disk_percent
        self.disk_label['text'] = f"Disk: {disk_percent:.1f}%"

    def check_alarms(self, cpu_percent, memory_percent, disk_percent):
        active_alarms = []

        for threshold in self.alarm_manager.alarms['CPU']:
            if cpu_percent > threshold:
                active_alarms.append(f"CPU usage ({cpu_percent:.1f}%) exceeds {threshold}%")

        for threshold in self.alarm_manager.alarms['Memory']:
            if memory_percent > threshold:
                active_alarms.append(f"Memory usage ({memory_percent:.1f}%) exceeds {threshold}%")

        for threshold in self.alarm_manager.alarms['Disk']:
            if disk_percent > threshold:
                active_alarms.append(f"Disk usage ({disk_percent:.1f}%) exceeds {threshold}%")

        self.alarms_text.delete(1.0, tk.END)
        if active_alarms:
            for alarm in active_alarms:
                self.alarms_text.insert(tk.END, alarm + "\n")
        else:
            self.alarms_text.insert(tk.END, "No active alarms")

    def run(self):
        self.create_gui()
        self.running = True
        self.update_thread = threading.Thread(target=self.update_values, daemon=True)
        self.update_thread.start()
        
        if self.root:
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.mainloop()

    def on_closing(self):
        self.running = False
        if self.root:
            self.root.quit()
            self.root.destroy()
        if self.update_thread:
            self.update_thread.join(timeout=2)

    def stop(self):
        self.running = False
        if self.root:
            self.root.quit()
        if self.update_thread:
            self.update_thread.join(timeout=2)