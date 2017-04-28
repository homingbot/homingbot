
import sys
import time
import config
import asyncio
from controller import server as api_server
from db import cassandra_util as db
from nest import smtp_server
import log
try:
    import uvloop as async_loop
except ImportError:
    async_loop = asyncio
from db import cassandra_util as db


logger = log.get_logger('Homingbot')
if config.dev_mode:
    logger.info("DEVELOPMENT MODE")
else:
    logger.info("Running in PRODUCTION")

logger.info("Version: [%s]" % config.version)



def __handle_args():
    to_launch = None
    if (len(sys.argv)) >= 2:
        to_launch = sys.argv[1]

    for i in range(2, len(sys.argv), 2):
        key = sys.argv[i][2:]
        setattr(config, key, (type(getattr(config, key)))(sys.argv[i+1]))
    return to_launch

if __name__ == '__main__':
    proc_to_launch = __handle_args()
    db.setup()
    loop = async_loop.new_event_loop()
    asyncio.set_event_loop(loop)

    if proc_to_launch == 'nest':
        loop.create_task(smtp_server.start(loop))
    elif proc_to_launch == 'controller':
        api_server.start(loop)
    else:
        loop.create_task(smtp_server.start(loop))
        api_server.start(loop)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
