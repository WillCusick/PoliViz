import json
import redis
from datetime import datetime, timedelta

max_tweets_per_load = 200
delimit = ":\\:"
len_delimit = len(delimit)

def geoFormat(red):
    tweets = red.smembers("tweets")
    json_dict = {'type': 'FeatureCollection',
                 'crs': {
                     'type': 'name',
                     'properties': {
                         'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'
                     }
                 },
                 'features': []
    }
    tweet_count = 0
    for tweet in tweets:
        if tweet_count >= max_tweets_per_load:
            break
        
        breaking_point = tweet.find(":\\:")
        
        time_added = datetime.strptime(tweet[breaking_point+len_delimit:], "%Y-%m-%d %H:%M:%S.%f")
        time_now = datetime.now()
        time_elapsed = time_now - time_added
        if time_elapsed.total_seconds() > 120:
            red.srem("tweets", tweet)
            continue
        
        tweet_json = {'type': 'Feature'}
        tweet_json['geometry'] = json.loads(tweet[:breaking_point].replace('\'','"'))
        tweet_json['properties'] = {'party': 'democrat'}
        json_dict['features'].append(tweet_json)
        tweet_count += 1
        
    return json_dict
