import pika
import json
import redis
from datetime import timedelta, datetime
from consumer import PoliConsumer

red = None
expiryTTL = timedelta(minutes=2)
candidate_dict = None
party_dict = None

def callback(ch, method, properties, body):
    data = json.loads(body)
    
    geoCoords = None
    if 'coordinates' in data and data['coordinates'] is not None:
        geoCoords = {'type': 'Point',
                  'coordinates': data['coordinates']['coordinates']}
    elif 'place' in data and data['place'] is not None:
        if 'bounding_box' in data['place'] and data['place']['bounding_box'] is not None:
            coordinates = data['place']['bounding_box']['coordinates'][0]
            num_c = len(coordinates)
            coords = [0.0, 0.0]
            # Note: faster to do one div at the end but may lose
            # some precision because floating-points are more
            # accurate closer to 0
            for c in coordinates:
                coords[0] += c[0]
                coords[1] += c[1]

            coords[0] /= num_c
            coords[1] /= num_c
            geoCoords = {'type':'Point', 'coordinates':coords}
    if geoCoords is not None:
        tweet = {'geometry': geoCoords,
                 'properties': categorize(data)}

        # Ignore people with no direct hashtags, very rare
        if bool(tweet['properties']):
            tweet['properties']['id'] = data['id']
            store(tweet)
             
def categorize(data):
    dict = {}
    for hash in data['hashtags']:
        if hash['text'].lower() in candidate_dict:
            dict['candidate'] = candidate_dict[hash['text'].lower()]
        if hash['text'].lower() in party_dict:
            dict['party'] = party_dict[hash['text'].lower()]
    return dict
            
def store(tweet):
    datastring = str(tweet) + ":\\:" + str(datetime.now()+expiryTTL)
    red.sadd("tweets", datastring)

if __name__ == "__main__":
    red = redis.StrictRedis(host='localhost', port=6379, db=0)

    candidate_dict = {'hillary2016': 'Hillary',
                      'hillaryforpresident': 'Hillary',
                      'clinton2016': 'Hillary',
                      'imwithher': 'Hillary',
                      'bernie2016': 'Bernie',
                      'bernieforpresident': 'Bernie',
                      'sanders2016': 'Bernie',
                      'voteberniesanders': 'Bernie',
                      'feelthebern': 'Bernie',
                      'debatewithbernie': 'Bernie',
                      'trump2016': 'Trump',
                      'donaldtrumpforpresident': 'Trump',
                      'trumpforpresident2016': 'Trump',
                      'votetrump2016': 'Trump',
                      'votetrump': 'Trump',
                      'makeamericagreatagain': 'Trump',
                      'bencarsonforprez': 'Carson',
                      'carson2016': 'Carson',
                      'omalley2016': 'OMalley',
                      'newleadership': 'OMalley',
                      'actionsnotwords': 'OMalley'}

    party_dict = {'hillary2016': 'democrat',
                  'hillaryforpresident': 'democrat',
                  'clinton2016': 'democrat',
                  'imwithher': 'democrat',
                  'bernie2016': 'democrat',
                  'bernieforpresident': 'democrat',
                  'sanders2016': 'democrat',
                  'voteberniesanders': 'democrat',
                  'feelthebern':'democrat',
                  'debatewithbernie': 'democrat',
                  'omalley2016': 'democrat',
                  'newleadership': 'democrat',
                  'actionsnotwords': 'democrat',
                  'donaldtrumpforpresident': 'republican',
                  'trump2016': 'republican',
                  'trumpforpresident2016': 'republican',
                  'votetrump2016': 'republican',
                  'votetrump': 'republican',
                  'makeamericagreatagain': 'republican',
                  'bencarsonforprez': 'republican',
                  'carson2016': 'republican'}
    
    rmq_connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    rmq_consumer = PoliConsumer(rmq_connection, callback)
    rmq_consumer.consume()
