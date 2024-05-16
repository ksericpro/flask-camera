import logging
import logging.config
import redis_manager
import sys
import datetime
#import importlib, os
#import common_fns
import config

init_inprogress = False
#LOG_MAX_SIZE = 50
#LOG_BACKUP = 12

def init(logfile_prefix, redis):
    global init_inprogress
    if (init_inprogress):
        print("[Init]::Process already started.")
        return

    init_inprogress = True

    print("[Init]::Setup Logger")
    # logger configuration
    global _logger
    global _rotatingHandler
    # Change root logger level from WARNING (default) to NOTSET in order for all messages to be delegated.
    logging.getLogger().setLevel(logging.NOTSET)

    # Add stdout handler, with level INFO
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    formater = logging.Formatter('%(name)-13s: %(levelname)-8s %(message)s')
    console.setFormatter(formater)
    logging.getLogger().addHandler(console)

    # Add file rotating handler, with level DEBUG

    _rotatingHandler = logging.handlers.RotatingFileHandler(
        filename=config.LOG_FOLDER + '/' + logfile_prefix + '-{:%Y-%m-%d}.log'.format(datetime.datetime.now()),
        maxBytes=(1048576 * config.LOG_MAX_SIZE), backupCount=config.LOG_BACKUP)
    _rotatingHandler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    _rotatingHandler.setFormatter(formatter)
    logging.getLogger().addHandler(_rotatingHandler)

    # Logger
    _logger = logging.getLogger("app." + __name__)

    if redis:
        _logger.info("[Init]::Setup Redis")
        global _redis_mgr
        _redis_mgr = redis_manager.RedisManager(_logger, config.REDIS_SERVER, config.REDIS_PORT, config.REDIS_PASSWORD)

    _logger.info("[Init]::Completed")