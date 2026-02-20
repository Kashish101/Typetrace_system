import logging
import os
import ftplib
import requests
import time
from datetime import datetime, timedelta


class LogUploader:
    def __init__(self, config):
        self.config = config
        self.transfer_method = config['transfer']['method']
        self.interval = config['transfer']['interval']
        self.running = False

    def _upload_ftp(self):
        try:
            ftp_config = self.config['ftp']
            with ftplib.FTP() as ftp:
                ftp.connect(ftp_config['host'], ftp_config['port'])
                ftp.login(ftp_config['username'], ftp_config['password'])
                ftp.cwd(ftp_config['remote_path'])

                for file in self._get_files_to_upload():
                    with open(file, 'rb') as f:
                        ftp.storbinary(f'STOR {os.path.basename(file)}', f)
                    os.remove(file)
                    logging.info(f"Uploaded and deleted: {file}")
        except Exception as e:
            logging.error(f"FTP upload failed: {e}")

    def _upload_https(self):
        try:
            https_config = self.config['https']
            headers = https_config['headers']
            headers['Authorization'] = f"Bearer {https_config['api_key']}"

            for file in self._get_files_to_upload():
                with open(file, 'rb') as f:
                    response = requests.post(
                        https_config['endpoint'],
                        headers=headers,
                        data=f.read()
                    )
                if response.status_code == 200:
                    os.remove(file)
                    logging.info(f"Uploaded and deleted: {file}")
                else:
                    logging.error(f"HTTPS upload failed: {response.status_code} - {response.text}")
        except Exception as e:
            logging.error(f"HTTPS upload failed: {e}")

    def _get_files_to_upload(self):
        log_dir = self.config['general'].get('log_dir', 'logs')
        retention = timedelta(days=self.config['general']['log_retention_days'])
        cutoff = datetime.now() - retention

        for filename in os.listdir(log_dir):
            filepath = os.path.join(log_dir, filename)
            if os.path.isfile(filepath) and os.path.getmtime(filepath) < cutoff.timestamp():
                yield filepath

    def start(self):
        self.running = True
        while self.running:
            if self.transfer_method == 'ftp':
                self._upload_ftp()
            elif self.transfer_method == 'https':
                self._upload_https()
            time.sleep(self.interval)

    def stop(self):
        self.running = False





