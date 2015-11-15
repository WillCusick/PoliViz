import json
import redis
from datetime import datetime, timedelta

max_tweets_per_load = 200
delimit = ":\\:"
len_delimit = len(delimit)

def prune(red, tweet):
    breaking_point = tweet.find(":\\:")
        
    time_added = datetime.strptime(tweet[breaking_point+len_delimit:], "%Y-%m-%d %H:%M:%S.%f")
    time_now = datetime.now()
    time_elapsed = time_now - time_added
    if time_elapsed.total_seconds() > 120:
        red.srem("tweets", tweet)
        return True
    return False

def geoFormat(red):
    if red.scard("tweets") > 2*max_tweets_per_load:
        for tweet in red.smembers("tweets"):
            prune(red, tweet)
    
    json_dict = {'type': 'FeatureCollection',
                 'crs': {
                     'type': 'name',
                     'properties': {
                         'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'
                     }
                 },
                 'features': []}
    
    tweet_count = 0
    for tweet in red.smembers("tweets"):
        if tweet_count >= max_tweets_per_load:
            break
        
        if prune(red, tweet):
            continue
        
        breaking_point = tweet.find(":\\:")
        tweet_json = json.loads(tweet[:breaking_point].replace('\'','"'))
        tweet_json['type'] = 'Feature'
        json_dict['features'].append(tweet_json)
        tweet_count += 1
        
    return json_dict

geoFormat(redis.StrictRedis(host='localhost', port=6379, db=0))
