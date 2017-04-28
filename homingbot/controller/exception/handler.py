from sanic.response import json
from sanic.exceptions import SanicException, InvalidUsage, NotFound
from cassandra.cqlengine.query import DoesNotExist
from controller import api
from controller.cors import add_cors
import log
import config
logger = log.get_logger(__name__)

@api.bp.exception(SanicException)
def sanic_exception(request, exception):
    return return_response(str(exception), exception.status_code)

@api.bp.exception(NotFound)
def sanic_exception_nf(request, exception):
    return return_response(str(exception), exception.status_code)

@api.bp.exception(InvalidUsage)
def sanic_exception_invalid(request, exception):
    return return_response(str(exception), exception.status_code)

@api.bp.exception(ValueError)
def value_error(request, exception):
    return return_response(str(exception), 400)

@api.bp.exception(DoesNotExist)
def dne_exception(request, exception):
    return return_response(str(exception), 404)


def return_response(message, status_code):
    response = json({"error": message}, status_code)
    return response
