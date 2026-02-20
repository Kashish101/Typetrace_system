# build in module to track events that happen during execution
import logging
# part of pynput library that monitors mouse input events
# like movements, clicks, scrolls
from pynput import mouse
# build in python module that helps us work with date and time
from datetime import datetime


class EnhancedMouseListener:
    # initializes the class with provided configurations
    def __init__(self, config):
        self.config = config
        self.log_file = f"{config['general'].get('log_dir', 'logs')}/mouse_{datetime.now().strftime('%Y%m%d')}.log"

# handles the formatting and writing of log entries
    def _log_event(self, event_type, **kwargs):
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            log_entry = f"{timestamp} - {event_type}: "
            log_entry += ", ".join([f"{k}={v}" for k, v in kwargs.items()])

# appends the formatted string to the log file
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + "\n")
                # else show the error message
        except Exception as e:
            logging.error(f"Mouse log error: {e}")

# called automatically when mouse moves
    def on_move(self, x, y):
        self._log_event("MOVE", x=x, y=y)

# called when the mouse button is pressed or released
    def on_click(self, x, y, button, pressed):
        self._log_event("CLICK", x=x, y=y, button=button.name, state="PRESSED" if pressed else "RELEASED")

# called when the mouse scroll wheel is used
    def on_scroll(self, x, y, dx, dy):
        # dx:dy is amount of scroll
        self._log_event("SCROLL", x=x, y=y, dx=dx, dy=dy)

# starts the mouse listener
    def start(self):
        listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll
        )
        listener.start()
        logging.info("Mouse listener started")
        return listener

