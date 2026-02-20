# import logging
# from pynput import keyboard
# from datetime import datetime
# from core.data_filter import DataFilter
#
#
# class EnhancedKeyboardListener:
#     # initializes the listener with configuration data
#     def __init__(self, config):
#         self.config = config
#         self.filter = DataFilter(config['security']['redact_patterns'])
#         self.log_file = self._init_log_file()
#
#
#
# # generates a log file name based on the current data
#     def _init_log_file(self):
#         log_dir = self.config['general'].get('log_dir', 'logs')
#         return f"{log_dir}/keystrokes_{datetime.now().strftime('%Y%m%d')}.log"
#
#
#
#
# # handles every key press event
#     def _on_press(self, key):
#         try:
#             log_entry = self._format_key(key)
#             filtered_entry = self.filter.redact(log_entry)
#             self._write_log(filtered_entry)
#         except Exception as e:
#             logging.error(f"Keyboard listener error: {e}")
#
#
#     # converts the key object into a string representation
#     def _format_key(self, key):
#         try:
#             return key.char
#         except AttributeError:
#             return f'[{key.name}]'
#
#
#
# # appends a new key log to the log file
#     def _write_log(self, entry):
#         try:
#             with open(self.log_file, 'a', encoding='utf-8') as f:
#                 timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
#                 f.write(f"{timestamp} - {entry}\n")
#         except IOError as e:
#             logging.error(f"Log write error: {e}")
#
#
# # starts the keyboard listener
#     def start(self):
#         listener = keyboard.Listener(on_press=self._on_press)
#         listener.start()
#         logging.info("Keyboard listener started")
#         return listener
#
#
#



import logging
from pynput import keyboard
from datetime import datetime
from pathlib import Path
from core.data_filter import DataFilter
import threading

class EnhancedKeyboardListener:
    def __init__(self, config):
        self.config = config
        self.filter = DataFilter(config['security']['redact_patterns'])
        self.log_file = self._init_log_file()
        self.buffer = ""
        self.listener = None
        self.flush_timer = None
        self.lock = threading.Lock()

    def _init_log_file(self):
        log_dir = self.config['general'].get('log_dir', 'logs')
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        return f"{log_dir}/keystrokes_{datetime.now().strftime('%Y%m%d')}.log"

    def _on_press(self, key):
        with self.lock:
            try:
                if hasattr(key, 'char') and key.char:
                    self.buffer += key.char
                elif key == keyboard.Key.space:
                    self.buffer += ' '
                elif key == keyboard.Key.enter:
                    self.buffer += '\n'
                elif key == keyboard.Key.backspace:
                    self.buffer = self.buffer[:-1]

                # Reset flush timer
                if self.flush_timer:
                    self.flush_timer.cancel()
                self.flush_timer = threading.Timer(2.0, self._flush_buffer)
                self.flush_timer.start()

            except Exception as e:
                logging.error(f"Keyboard listener error: {e}")

    def _flush_buffer(self):
        with self.lock:
            if self.buffer.strip():
                redacted = self.filter.redact(self.buffer.strip())
                self._write_log(redacted + '\n')
                self.buffer = ""

    def _write_log(self, entry):
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                f.write(f"{timestamp} - {entry}")
        except IOError as e:
            logging.error(f"Log write error: {e}")

    def start(self):
        if self.listener is None:
            self.listener = keyboard.Listener(on_press=self._on_press)
            self.listener.daemon = True
            self.listener.start()
