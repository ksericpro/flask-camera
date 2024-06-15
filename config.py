#API
API_KEY = "btehsjqnhrdvghjqciebrffbkrxagvuy"

#SSL
USE_SSL = False

# Playback
#img_url = "D:/projects/dotnetprojects/dotnet-bodywornsln/files"
PLAYBACK_IMAGE_SRC = "D:/projects/dotnetprojects/dotnet-bodywornsln/files"
PLAYBACK_CAMERA_DELAY_START = 3
#PLAYBACK_PERIOD = 5
PLAYBACK_PERIOD = 5
PLAYBACK_FPS = 2
PLAYBACK_DELETE_SRC_IMAGE_COMMIT = True

#redis
REDIS_SERVER = "127.0.0.1"
REDIS_PORT = 6379
REDIS_PASSWORD = ''
REDIS_BWC_TOPIC = "/BWC"
REDIS_WAIT_SECONDS = 10

# Flask
FLASK_PORT = 5000
API_PREFIX = "/bwc"
LOG_FOLDER = "logs"
LOG_MAX_SIZE = 50
LOG_BACKUP = 12
FLASK_DEBUG = False
API_VERSION= 'v1'
APPLICATION_NAME = "BWC Manage"
APPLICATION_VERSION = "v1.0.0"