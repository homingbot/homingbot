from aiosmtpd.controller import Controller
from aiosmtpd.smtp import SMTP
import config
import socket
import threading
import asyncio
import ssl

def get_tls_context():
    tls_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    tls_context.load_cert_chain(config.nest_tls['cert'], config.nest_tls['key'])
    return tls_context

class SMTPController(Controller):
    def __init__(self, handler, loop=None, hostname='::0', port=8025, ready_timeout=1.0):
        self.handler = handler
        self.hostname = '::1' if hostname is None else hostname
        self.port = port
        self.loop = asyncio.new_event_loop() if loop is None else loop
        self.server = None
        self.thread = None
        self.thread_exception = None
        self.ready_timeout = ready_timeout
        # For exiting the loop.
        self._rsock, self._wsock = socket.socketpair()
        self.loop.add_reader(self._rsock.fileno(), self._reader)


    def factory(self):
        """Allow subclasses to customize the handler/server creation."""
        return SMTP(self.handler, loop=self.loop, data_size_limit=config.max_data_size,
                    tls_context=get_tls_context() if config.use_tls else None, require_starttls = config.use_tls)
