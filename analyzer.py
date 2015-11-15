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
        store(tweet)
             
def categorize(data):
    dict = {}
    for hash in data['hashtags']:
        if hash['text'] in candidate_dict:
            dict['candidate'] = candidate_dict[hash['text']]
        if hash['text'] in party_dict:
            dict['party'] = party_dict[hash['text']]
    return dict
            
def store(tweet):
    datastring = str(tweet) + ":\\:" + str(datetime.now()+expiryTTL)
    red.sadd("tweets", datastring)

if __name__ == "__main__":
    red = redis.StrictRedis(host='localhost', port=6379, db=0)

    candidate_dict = {'Hillary2016': 'Hillary',
                      'HillaryForPresident': 'Hillary',
                      'Clinton2016': 'Hillary',
                      'ImWithHer': 'Hillary',
                      'Bernie2016': 'Bernie',
                      'BernieForPresident': 'Bernie',
                      'Sanders2016': 'Bernie',
                      'VoteBernieSanders': 'Bernie',
                      'FeelTheBern': 'Bernie',
                      'DebateWithBernie': 'Bernie',
                      'Trump2016': 'Trump',
                      'DonaldTrumpForPresident': 'Trump',
                      'Trump2016': 'Trump',
                      'TrumpForPresident2016': 'Trump',
                      'VoteTrump2016': 'Trump',
                      'VoteTrump': 'Trump',
                      'MakeAmericaGreatAgain': 'Trump',
                      'BenCarsonForPrez': 'Carson',
                      'Carson2016': 'Carson',
                      'OMalley2016': 'OMalley',
                      'NewLeadership': 'OMalley',
                      'ActionsNotWords': 'OMalley'}

    party_dict = {'Hillary2016': 'democrat',
                  'HillaryForPresident': 'democrat',
                  'Clinton2016': 'democrat',
                  'ImWithHer': 'democrat',
                  'Bernie2016': 'democrat',
                  'BernieForPresident': 'democrat',
                  'Sanders2016': 'democrat',
                  'VoteBernieSanders': 'democrat',
                  'FeelTheBern':'democrat',
                  'DebateWithBernie': 'democrat',
                  'OMalley2016': 'democrat',
                  'NewLeadership': 'democrat',
                  'ActionsNotWords': 'democrat',
                  'DonaldTrumpForPresident': 'republican',
                  'Trump2016': 'republican',
                  'TrumpForPresident2016': 'republican',
                  'VoteTrump2016': 'republican',
                  'VoteTrump': 'republican',
                  'MakeAmericaGreatAgain': 'republican',
                  'BenCarsonForPrez': 'republican',
                  'Carson2016': 'republican'}
    
    rmq_connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    rmq_consumer = PoliConsumer(rmq_connection, callback)
    rmq_consumer.consume()
