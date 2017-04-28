from models import mail
from .names import list1
import arrow
import random
import config
r = random.SystemRandom()

def generate_emails(n):
    while(n > 0):
        yield mail.Email(
            address='%s_%s@%s' % (r.choice(list1.left), r.choice(list1.right), config.email_host),
            created=arrow.utcnow().datetime
        )
        n -= 1
