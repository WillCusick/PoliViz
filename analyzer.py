import pika
import json
from consumer import PoliConsumer

def callback(ch, method, properties, body):
    data = json.loads(body)
    # if 'coordinates' in data and data['coordinates'] is not None:
    #     print "Coords %s" % data['coordinates']
    # elif 'place' in data and data['place'] is not None:
    #     if 'bounding_box' in data['place'] and data['place']['bounding_box'] is not None:
    #         coordinates = data['place']['bounding_box']['coordinates'][0]
    #         num_c = len(coordinates)
    #         coords = [0.0, 0.0]
    #         # Note: faster to do one div at the end but may lose
    #         # some precision because floating-points are more
    #         # accurate closer to 0
    #         for c in coordinates:
    #             coords[0] += c[0]
    #             coords[1] += c[1]

    #         coords[0] /= num_c
    #         coords[1] /= num_c
    #         print "Place %s" % coords
    print data

if __name__ == "__main__":
    rmq_connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    rmq_consumer = PoliConsumer(rmq_connection, callback)
    rmq_consumer.consume()
