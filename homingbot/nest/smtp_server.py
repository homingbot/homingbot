import log
import asyncio
import re
import uuid
import arrow
import config
import logging
from models.mail import Email, Message
from db import cassandra_util as db_service
from aiosmtpd.handlers import AsyncMessage
from nest.smtp_controller import SMTPController
from utils import common_utils

try:
    import uvloop as async_loop
except ImportError:
    async_loop = asyncio

logger = log.get_logger(__name__)
STATUS_OK = "250 OK"
STATUS_NO_STORAGE = "422"
STATUS_ERROR = "451"
STATUS_UNAVAILABLE = "550 USER NOT FOUND"

EMAIL_REGEX = "^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$"
REGEX = re.compile(EMAIL_REGEX)
EMAIL_QUERY_TEMPLATE = "SELECT address, TTL(created) FROM %s.emails WHERE address in ({});" % config.cassandra_keyspace
COUNT_QUERY_TEMPLATE = "SELECT count(address) FROM %s.messages WHERE address = '{}';" % config.cassandra_keyspace

def deal_with_multipart(data):
    if data.is_multipart():
        res = ""
        for payload in data.get_payload():
            res += (deal_with_multipart(payload) + "" if res == "" else "\n")
        return res
    else:
        return data.get_payload()

class SMTPServer(AsyncMessage):
    async def handle_DATA(self, server, session, envelope):
        envelope = self.prepare_message(session, envelope)
        return self.handle_message(envelope)

    def handle_message(self, message):
        if (message['X-MailFrom'] is None or message['X-RcptTo'] is None):
            return STATUS_ERROR
        sender_ip = message['X-Peer'] #TODO check blacklist
        logger.info("Incomming from: %s", sender_ip)
        sender = message['X-MailFrom'] #TODO check blacklist
        to =  message['X-RcptTo'].split(", ")
        valid_emails = list(filter(REGEX.match, to))
        email_set = str(valid_emails)[1:-1]
        res = db_service.custom_query(EMAIL_QUERY_TEMPLATE.format(email_set))
        if (res is None):
            return STATUS_UNAVAILABLE
        emails_found = res.current_rows
        if (len(emails_found) < 1):
            return STATUS_UNAVAILABLE
        print(message)
        data = deal_with_multipart(message)
        print(data)
        self.process_message(sender, emails_found, data)
        return STATUS_OK

    def process_message(self, mailfrom, rcpttos, data):
        email = None
        messages = []
        emails = []
        splitted = data.split("\r\n", 1)
        subject = splitted[0] if (len(splitted) > 0) else ""
        body = splitted[1] if (len(splitted) > 1) else ""
        try:
            for recipient in rcpttos:
                num_emails = 0
                res = db_service.custom_query(COUNT_QUERY_TEMPLATE.format(recipient['address'])) #TODO async
                if (res is not None and len(res.current_rows) > 0):
                    num_emails = res.current_rows[0]['system.count(address)']
                msg = Message(address=recipient['address'], message_index=num_emails, body=data, size=len(data), sender=mailfrom, created=arrow.utcnow().datetime)
                messages.append(msg)
            db_service.batch_save(messages, ttl=recipient['ttl(created)']) # Save with the ttl of the email account
        except Exception as e:
            logger.error(e)
            return STATUS_ERROR
        return STATUS_OK


server = None

async def start(loop):
    global server
    server = SMTPController(SMTPServer(), hostname=config.nest_host, port=config.nest_port)
    server.start()
    logger.info("Starting smtp server on port %s", config.nest_port)
    logger.info("TLS: [%s]" % config.use_tls )
    logger.info("Successfully started SMTP server")

def stop():
    global server
    server.stop()

if __name__ == '__main__':
    start()
