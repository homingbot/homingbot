from sanic import Sanic
import log
from . import security, api
from .exception import handler

import config

logger = log.get_logger(__name__)

app = Sanic("HomingBot")
app.log = logger
app.blueprint(api.bp)
security.PostSecurity(app)

def start(loop):
    logger.info("Starting api server...")
    app.run(host=config.host, port=config.port, workers=config.workers, debug=config.dev_mode, loop=loop)
