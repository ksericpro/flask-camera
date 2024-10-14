import redis
import metaclass
import time
import threading
import common_fns
import config

class RedisManager(object):
    __metaclass__ = metaclass.SingletonMetaClass
    def __init__(self, logger, redis_uri, redis_port, redis_password):
        self.logger = logger
        self.name = "Redis Manager"
        self.redis_uri = redis_uri
        self.redis_port = redis_port
        self.redis_password = redis_password
        #self.connected = self.connect(self.redis_uri, self.redis_port, self.redis_password)
        self.connected = False
        self.connect_server()
        self.timer = None

    def __del__(self):
        self.logger.info(self.name + ' died')

    def cleanup(self):
        if self.timer is not None:
            self.timer.cancel()
        self.logger.info(self.name + ' cleanup')

    def __str__(self):
        return 'self' + self.name

    def connect_server(self):
        self.connected = self.connect(self.redis_uri, self.redis_port, self.redis_password)
        if not self.connected:
            self.timer = threading.Timer(config.REDIS_WAIT_SECONDS, self.connect_server)
            self.timer.start()
        #print("xxx", self.timer)

    def connect(self, redis_uri, redis_port, redis_password):
        try:
            self.logger.info("{0}::Trying to Connected to '{1}:{2}:{3}'".format(self.name, redis_uri, redis_port, redis_password))
            self.client = redis.StrictRedis(host=redis_uri, port=redis_port, password=redis_password)
            ping = self.client.ping()
            self.logger.info('%s::Successfully connected.' % self.name)
            return True
        except:
            self.logger.error('%s::Fail to connect.'%self.name)
            return False

    def publish(self, topic, message):
        try:
            #p = self.client.pubsub()

            if (not self.connected):
                #self.logger.info('%s::Trying to connect'%self.name)
                self.connected = self.connect(self.redis_uri, self.redis_port, self.redis_password)

            if (self.connected):
                info = common_fns.shortened_string(message, 1000)
                self.logger.info("%s::Publishing '%s' to '%s'" % (self.name, info, topic))
                self.client.publish(topic, message)
            else:
                self.logger.info('%s::Message not sent.'%self.name)
        except Exception as e:
            self.logger.error(str(e))
            #print(traceback.format_exc())

    def subscribe(self, topic):
        try:
            if (not self.connected):
                #self.logger.info('%s::Trying to connect' % self.name)
                self.connected = self.connect(self.redis_uri, self.redis_port, self.redis_password)

            if (self.connected):
                p = self.client.pubsub()
                self.logger.info("%s::Subscribing %s" % (self.name, topic))
                p.subscribe([topic])
                while True:
                    message = p.get_message()

                    if message is not None:
                        if (message['type']=='message'):
                            print("Subscriber: %s" % message['data'])
                    time.sleep(1)
        except Exception as e:
            self.logger.error(str(e))