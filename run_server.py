from flask import Flask
from flask import render_template
from flask import jsonify
from jsoncreator import geoFormat
import redis
import json
app = Flask(__name__)

red = None

@app.route('/')
def home_page():
    return render_template('index3.html')

@app.route('/tweets.json')
def tweets():
    json_dict = geoFormat(red)
    return jsonify(json_dict)
    
if __name__ == '__main__':
    red = redis.StrictRedis(host='localhost', port=6379, db=0)
    app.run()
