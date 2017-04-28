import os
import sys
import imp
import inspect
import config
from datetime import datetime
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine.columns import UUID
from cassandra.cqlengine import connection
from cassandra.cqlengine import management
from cassandra.cqlengine.query import BatchQuery
from cassandra.cqlengine.connection import execute
from cassandra.util import uuid_from_time
import models
from models import json_model as BaseModel
import log
import ssl

logger = log.get_logger('DB.CASSANDRA')

MAX_BATCH_SIZE = 1200

def str_to_uuid(id):
    result = None
    try:
        result = UUID().validate(id)
    except Exception as e:
        pass
    finally:
        return result

def generate_time_uuid():
    return uuid_from_time(datetime.now())


def custom_query(query):
    return execute(query)

def batch_save(models, ttl = None):
    ''' Executes the batch query '''
    if len(models) <= MAX_BATCH_SIZE:
        b = BatchQuery()
        for m in models:
            if (ttl is not None):
                m.batch(b).ttl(ttl).save()
            else:
                m.batch(b).save()
        b.execute()
    else:
        start = 0
        end = MAX_BATCH_SIZE
        while end <= len(models):
            batch_save(models[start : end])
            start = end
            if end == len(models):
                break
            end =  len(models) if (end+MAX_BATCH_SIZE) > len(models) else end+MAX_BATCH_SIZE;


def setup():
    auth_provider = PlainTextAuthProvider(username=config.cassandra_user, password=config.cassandra_password)
    res = None
    if config.dev_mode:
        res = connection.setup(config.cassandra_hosts, config.cassandra_keyspace, protocol_version=3)
    else:
        logger.info("Using cert: %s", config.cassandra_client_cert)
        logger.info("Using key: %s", config.cassandra_client_key)

        res = connection.setup(
            config.cassandra_hosts,
            config.cassandra_keyspace,
            protocol_version=3,
            auth_provider=auth_provider,
            ssl_options={
                'keyfile': config.cassandra_client_key,
                'certfile': config.cassandra_client_cert,
                'ssl_version': ssl.PROTOCOL_TLSv1,
            }
        )
    print(res)
    if (config.dev_mode):
        management.create_keyspace_simple(config.cassandra_keyspace, 1)
        logger.debug("Processing tables...")
        for module, _ in inspect.getmembers(models, inspect.ismodule):
            for name, model in inspect.getmembers(models.__dict__[module], inspect.isclass):
                if not model.__dict__.get('__ignore__', False) and issubclass(model, BaseModel.Model):
                    logger.debug("Syncing table %s", name)
                    management.sync_table(model)
    logger.info("Successfully setup Cassandra!")

if __name__ == '__main__':
    setup()
