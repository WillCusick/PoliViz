import pika

class PoliConsumer(object):
    pass

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)

connection = pika.BlockingConnection(pika.ConnectionParameters(
    'localhost'))
channel = connection.channel()

channel.queue_declare(queue='tweets')
channel.basic_consume(callback,
                      queue='tweets',
                      no_ack=True)

print '[*] Waiting for messages. To exit press CTRL+C'
channel.start_consuming()
