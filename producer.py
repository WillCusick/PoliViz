import pika

class PoliProducer(object):
    def __init__(self, connection, channel_name='tweets'):
        self.connection = connection
        self.channel = connection.channel()
        self.routing_key = channel_name
        self.channel.queue_declare(queue=channel_name)

    def produce(self, body):
        self.channel.basic_publish(exchange='',
                              routing_key=self.routing_key,
                              body=body)

    def __del__(self):
        self.connection.close()        
