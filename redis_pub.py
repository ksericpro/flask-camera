import redis

# Connect to local Redis instance
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
channel = 'my_channel'
while True:
    message = input("Enter a message: ")
    redis_client.publish(channel, message)