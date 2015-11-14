import tweepy
import time
import json
import sys

def echo(arg):
    print arg

class PoliStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status.author.lang == 'en':
            message = {'author_name': status.author.screen_name,
                       'author_id': status.author.id,
                       'id': status.id,
                       'text': status.text,
                       'coordinates': status.coordinates,
                       'place': status.place,
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
        print "Deleted"

    def set_callback(self, callback):
        self.callback = callback

class PoliReceiver(object):
    def setup(self, auth):
        print "Running"
        listener = PoliStreamListener()
        listener.set_callback(echo)
        self.stream = tweepy.Stream(auth, listener, timeout=3600)

    def stream_filter(self):
        while True:
            try:
                self.stream.filter(track=['#paris'])
            except Exception as e:
                print "Exception", e
                time.sleep(10)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        conf_file_name = sys.argv[1]
    else:
        conf_file_name = "twit_api.conf"

    config = {}
    with open(conf_file_name) as conf:
        for line in conf:
            sep = line.index('=')
            conf_option_name = line[:sep]
            config[conf_option_name] = line[sep+1:].rstrip()

    receiver = PoliReceiver()
    auth = tweepy.OAuthHandler(config['consumer_key'],config['consumer_secret'])
    auth.set_access_token(config['access_token_key'], config['access_token_secret'])
    receiver.setup(auth)
    receiver.stream_filter()
