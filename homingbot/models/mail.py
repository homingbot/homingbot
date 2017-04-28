import config
from .json_model import JsonModel
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class Email(JsonModel):
    __table_name__ = "emails"
    __options__ = {'default_time_to_live': config.ttl}
    address = columns.Text(primary_key=True, partition_key=True)
    created = columns.DateTime()

class Message(JsonModel):
    __table_name__ = "messages"
    __options__ = {'default_time_to_live': config.ttl}
    address  = columns.Text(primary_key=True, partition_key=True)
    # message_id = columns.TimeUUID(primary_key=True, clustering_order="DESC")
    message_index = columns.Integer(primary_key=True, clustering_order="DESC")
    subject = columns.Text()
    body = columns.Text()
    size = columns.Integer()
    sender = columns.Text()
    created = columns.DateTime()
