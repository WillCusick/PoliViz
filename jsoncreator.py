import json
import redis

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
    for tweet in tweets:
        tweet_json = {'type': 'Feature'}
        breaking_point = tweet.find(":\\:")
        tweet_json['geometry'] = json.loads(tweet[:breaking_point].replace('\'','"'))
        tweet_json['properties'] = {'party': 'democrat'}
        json_dict['features'].append(tweet_json)
        
    return json_dict
