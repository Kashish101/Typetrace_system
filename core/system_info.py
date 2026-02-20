import psutil
import platform
from datetime import datetime
import os
import logging

class SystemInfo:
    def get_cpu_usage(self):
        """Return CPU usage percentage"""
        return psutil.cpu_percent(interval=1)

    def get_memory_usage(self):
        """Return memory usage percentage"""
        return psutil.virtual_memory().percent

    def get_disk_usage(self):
        try:
            root_path = os.path.abspath(os.sep)
            return psutil.disk_usage(root_path).percent
        except Exception as e:
            logging.error(f"Disk monitoring error: {e}")
            return 0  # Return default value

    def get_system_uptime(self):
        """Return system uptime in seconds"""
        return datetime.now().timestamp() - psutil.boot_time()

    def get_network_stats(self):
        """Return network statistics"""
        net_io = psutil.net_io_counters()
        return {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv
        }