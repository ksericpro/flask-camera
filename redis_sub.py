import redis
import config

# Connect to local Redis instance
redis_client = redis.StrictRedis(host=config.REDIS_SERVER, port=config.REDIS_PORT, db=0)
channel = config.REDIS_BWC_TOPIC
pubsub = redis_client.pubsub()
pubsub.subscribe(channel)
print(f"Subscribed to {channel}. Waiting for messages...")
for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"Received: {message['data'].decode('utf-8')}")