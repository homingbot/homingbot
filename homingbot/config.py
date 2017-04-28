# Configuration file
import os
import logging


'''
All times are in seconds
'''
version = '1.0.0'
#======Controller============
workers = 1
host = '0.0.0.0'
port = os.getenv('CONTROLLER_PORT', 8080)
date_format = 'YYYY-MM-DD HH:mm:ss ZZ'
mode = os.getenv('MODE', 'DEV')
dev_mode = mode == 'DEV'

#Cors
enable_cors = False
cor_origins = "localhost"
cor_methods = 'POST, GET'
cor_headers = 'Authorization, Content-Type'
cor_creds = 'true'
cor_max_age = '300'

#==========Nest==============
host_v4 = host
host_v6 = '::1'
nest_port = os.getenv('NEST_PORT', 46500)
enable_ipv6 = False #TODO fix ipv6 problem
ttl = int(os.getenv('TTL', 1800))
listen_time = 15
nest_host = host_v6 if enable_ipv6 else host_v4
max_data_size = 33554432
use_tls = os.getenv('TLS', False) == 'True'
nest_tls = {
    'cert': os.getenv('NEST_CERT', '/certs/nest.cert'),
    'key': os.getenv('NEST_KEY', '/certs/nest.key')
}
email_host = os.getenv('NEST_EMAIL_HOST', 'homingbot.test')

#==========Databases===============
# Cassandra
cassandra_hosts = os.getenv('CASSANDRA_HOST', '192.168.0.2').split(',')
cassandra_port = '9042'
cassandra_keyspace = 'homingbot_test'
cassandra_user = os.getenv('CASSANDRA_USER', 'cassandra')
cassandra_password = os.getenv('CASSANDRA_PASSWORD', 'cassandra')
cassandra_client_cert = os.getenv('CASSANDRA_CLIENT_CRT', '/certs/client.crt')
cassandra_client_key = os.getenv('CASSANDRA_CLIENT_KEY', '/certs/client.key')
os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = 'False'

#============logging===========
#Levels
log_levels = {
    'Sanic': logging.INFO,
    'cassandra': logging.WARN,
    'Homingbot': logging.INFO,
    'mail.log': logging.WARN,
    'nest.smtp_server': logging.INFO,
    'CASS': logging.WARN
}
