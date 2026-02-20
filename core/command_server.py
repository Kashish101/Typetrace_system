import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading

class CommandHandler(BaseHTTPRequestHandler):
    def __init__(self, config, *args, **kwargs):
        self.config = config
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            "status": "active",
            "settings": {
                "screenshot_interval": self.config['general']['screenshot_interval'],
                "transfer_method": self.config['transfer']['method']
            }
        }
        self.wfile.write(json.dumps(response).encode())

class CommandServer:
    def __init__(self, config):
        self.config = config
        self.server = None
        self.thread = None

    def start(self):
        port = self.config.get('command_port', 8080)
        handler = lambda *args: CommandHandler(self.config, *args)
        self.server = HTTPServer(('', port), handler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()
        logging.info(f"Command server started on port {port}")

    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            logging.info("Command server stopped")