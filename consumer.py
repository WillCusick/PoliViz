import pika

class HRConsumer(object):
    def __init__(self, connection, callback, channel_name='tweets'):
        self.connection = connection
        self.channel = connection.channel()
        self.channel_name = channel_name
        self.channel.queue_declare(queue=channel_name)
        self.callback = callback

    def consume(self):
        self.channel.basic_consume(self.callback,
                                   queue=self.channel_name,
                                   no_ack=True)
        self.channel.start_consuming()

    def __del__(self):
        self.connection.close()

    def set_callback(self, callback):
        self.callback = callback
