# HashRace
Visualization of the epic battles that occur on the Twittersphere!

HashRace captures in real-time what's going on in your friendly neighborhood hashtag races. We store the last 5 minutes of Tweets and display them on a map for you! Users can click on individual markers to be linked to the individual Tweets!

We are demoing this application with the Democratic Debate. The hashtags of popular candidates in the debate are tracked and colorized. We even track some of your favorite republican candidates!

# Demo
[Youtube video](https://youtu.be/mNBN7szEfmA)

[Image](http://i.imgur.com/RBMNe4w.jpg)

# Installation
## Dependencies
HashRace has the following Python library dependencies:

- Flask
- Redis-py
- Pika
- Tweepy

These can be installed with pip/easy_install

      sudo pip install flask redis pika tweepy

HashRace is also dependent on RabbitMQ and Redis. For information on how to install them, refer to their websites. RabbitMQ and Redis must be running on localhost and default ports for HashRace to recognize them.

Finally, to install HashRace, just clone this git repository.

# Running
 First, make sure RabbitMQ and Redis are running. Then simply run the following:

 	python receiver.py & python analyzer.py & python run_server.py

Open your favorite browser to http://127.0.0.1:5000/

