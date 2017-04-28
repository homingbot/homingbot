from sanic.response import json, text
from sanic import Blueprint
from sanic.views import HTTPMethodView
from sanic.exceptions import InvalidUsage, NotFound
from validate_email import validate_email

from models import mail
from db import cassandra_util as db_service
from utils import common_utils
from . import utils
import log
import config
import arrow

logger = log.get_logger(__name__)
LATEST = "latest"
bp = Blueprint('api')

def parse_id(id):
    """
    Parses id into a email
    """
    if validate_email(id, check_mx=False):
        return str(id)
    return None

def get_email(id):
    try:
        return mail.Email.objects(address=id).get()
    except (mail.Email.DoesNotExist, KeyError):
        raise NotFound('could not find email with address %s' % (id))
    return email

def get_message(id, index):
    result = {}
    try:
        result['count'] = 1
        if (index >= 0):
            message = mail.Message.objects(address=id, message_index=index).get()
            if (message is None):
                raise mail.Message.DoesNotExist()
            result['messages'] = [message.toJson()]
    except (mail.Message.DoesNotExist, KeyError):
        raise NotFound('could not find message index %s for email %s' % (index, id))
    except (mail.Email.DoesNotExist, KeyError):
        raise NotFound('could not find email with address %s' % (id))
    return json(result)

def get_messages(id):
    result = {}
    try:
        messages = mail.Message.filter(address=id)
        if (len(messages) == 0):
            raise NotFound('could not find messages for email %s' % ( id))

        result['count'] = len(messages)
        msg_list = []
        for msg in messages:
            msg_list.append(msg.toJson())
        result['messages'] = msg_list
    except (mail.Message.DoesNotExist, KeyError):
        raise NotFound('could not find messages for email %s' % ( id))
    except (mail.Email.DoesNotExist, KeyError):
        raise NotFound('could not find email with address %s' % (id))
    return json(result)

def get_post_param(request, param):
    data = None
    val = None
    data = request.form
    if len(data) == 0:
        data = request.json
        val = data[param]
    else:
        val = data[param][0]
    if (val is None):
        raise ValueError("could not find param %s" % param)
    return val

@bp.route('/accounts', methods=["GET"])
async def getActiveAccounts(request):
    '''
    Get all emails belonging to user
    '''
    emails = mail.Email.all()
    res = []
    for email in emails:
        json_res = email.toJson()
        created = arrow.get(email.created).timestamp
        now = arrow.utcnow().timestamp
        json_res['ttl'] = config.ttl - (now - created)
        res.append(json_res)
    return json({'accounts': res, 'count': len(res)})

@bp.route('/generate', methods=["POST"])
async def get(request):
    '''
    Generate x number of emails
    '''
    count = int(get_post_param(request, 'count'))
    try:
        if count <= 0:
            raise InvalidUsage('count must be greater than 0')
    except KeyError:
        raise InvalidUsage('count must be present')
    live_emails = mail.Email.all()
    logger.debug("Generating %s emails.", count)
    email_gen = utils.generate_emails(count)
    emails = []
    addresses = []
    for n in range(count):
        email = next(email_gen)
        emails.append(email)
        addresses.append(email.address)
    db_service.batch_save(emails)
    return json({'accounts': addresses, "total_active": len(live_emails) + count}, status = 201)


@bp.route('/emails', methods=["POST"])
async def getEmails(request):
    id = get_post_param(request, 'account')
    index = None
    try:
        index = get_post_param(request, 'index')
    except KeyError:
        pass

    id = parse_id(id)
    i = 0
    if (id is None):
        raise InvalidUsage('provide a valid email address')

    if index is not None:
        i = int(index)
        if (i < 0):
            raise InvalidUsage('index must be greater or equal to 0')
        return get_message(id, i)
    else:
        return get_messages(id)
