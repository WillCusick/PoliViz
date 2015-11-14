import tweepy
import time
import json
import argparse
from producer import PoliProducer
import pika

class PoliStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        # Re-box the place and bounding box information because
        # Tweepy's models are not JSON-serializable
        if status.place is not None:
            if status.place.bounding_box is not None:
                bounding_box = {'coordinates':
                                status.place.bounding_box.coordinates}
            else:
                bounding_box = None
        
            place = {'country_code': status.place.country_code,
                     'url': status.place.url,
                     'place_type': status.place.place_type,
                     'bounding_box': bounding_box,
                     'full_name': status.place.full_name,
                     'name': status.place.name}
        else:
            place = None
        
        message = {'author_name': status.author.screen_name,
                   'author_id': status.author.id,
                   'id': status.id,
                   'text': status.text,
                   'coordinates': status.coordinates,
                   'place': place,
                   'time': int(time.time())}
        self.callback(json.dumps(message))
            
    def on_connect(self):
        print "Connected"

    def on_error(self, status_code):
        print status_code

    def on_timeout(self):
        print "Timeout"

    def on_limit(self, track):
        print "Limited"

    def on_delete(self, status_id, user_id):
        #print "Deleted"
        pass

    def set_callback(self, callback):
        self.callback = callback

class PoliReceiver(object):
    def setup(self, auth, callback):
        print "Running"
        listener = PoliStreamListener()
        listener.set_callback(callback)
        self.stream = tweepy.Stream(auth, listener, timeout=3600)

    def stream_filter(self, tracking):
        while True:
            try:
                self.stream.filter(track=tracking)
                # self.stream.sample()
            except Exception as e:
                print "Exception", e
                time.sleep(10)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Receive Twitter Stream API events')
    parser.add_argument('-c', '--conf', nargs='?',
                        default='twit_api.conf',
                        help='location of config file containing API keys')
    parser.add_argument('hashtag', nargs='+',
                        help='list of hashtags to track')
    args = vars(parser.parse_args())
    print args
    
    config = {}
    with open(args['conf']) as conf:
        for line in conf:
            sep = line.index('=')
            conf_option_name = line[:sep]
            config[conf_option_name] = line[sep+1:].rstrip()

    rmq_connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    rmq_producer = PoliProducer(rmq_connection)

    receiver = PoliReceiver()
    auth = tweepy.OAuthHandler(config['consumer_key'],
                               config['consumer_secret'])
    auth.set_access_token(config['access_token_key'],
                          config['access_token_secret'])
    receiver.setup(auth, rmq_producer.produce)
    receiver.stream_filter(args['hashtag'])
