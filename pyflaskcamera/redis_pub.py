import redis
import config

# Connect to local Redis instance
redis_client = redis.StrictRedis(host=config.REDIS_SERVER, port=config.REDIS_PORT, db=0)
#redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
channel = config.REDIS_BWC_TOPIC
while True:
    message = input("Enter a message: ")
    redis_client.publish(channel, message)