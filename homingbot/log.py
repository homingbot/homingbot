import logging
import config


formatter = logging.Formatter('%(asctime)-15s - [%(levelname)s] - %(name)13s:%(lineno)-5s - %(message)s')

def get_logger(name):
    logger = logging.getLogger(name)
    logger.propagate = False
    log_level = None
    if name not in config.log_levels.keys():
        log_level = logging.DEBUG
    else:
        log_level = config.log_levels[name]
    logger.setLevel(log_level)
    if config.mode == 'PROD':
        fh = logging.FileHandler('homingbot.log')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    # create formatter and add it to the handlers
    return logger
