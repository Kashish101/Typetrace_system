import logging
import time
import os
from PIL import ImageGrab
from datetime import datetime

class ScreenshotManager:
    def __init__(self, config):
        self.config = config
        self.screenshot_dir = self._create_screenshot_dir()
        self.interval = config['general']['screenshot_interval']
        self.running = False

    def _create_screenshot_dir(self):
        screenshot_dir = self.config['general'].get('screenshot_dir', 'screenshots')
        os.makedirs(screenshot_dir, exist_ok=True)
        return screenshot_dir

    def _capture(self):
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{self.screenshot_dir}/screen_{timestamp}.png"
            ImageGrab.grab().save(filename)
            logging.info(f"Screenshot captured: {filename}")
        except Exception as e:
            logging.error(f"Screenshot capture failed: {e}")

    def start(self):
        self.running = True
        while self.running:
            self._capture()
            time.sleep(self.interval)

    def stop(self):
        self.running = False