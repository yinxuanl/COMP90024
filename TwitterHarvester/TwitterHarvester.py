import time

import couchdb
import tweepy
import sys
import methods

# settings for Twitter API authentication
CONSUMER_KEY = 'R8Huo0RRHNfcGaXbEcWfKHjmg'
CONSUMER_SECRET = 'OFvsIk4SeLvLk3YhfZiieLumhteu9javO4DTsLJwUdJSd2OBBg'
ACCESS_TOKEN = '942702516805943296-CY5fdJ5N5UZ3FiLGIlj0b9U0jH39ak2'
ACCESS_TOKEN_SECRET = '2yK7u81Ia4NbWtR21GtQ1lJyKwxfqTDIO332Q6NGRlOUA'

# authentication for Twitter API
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# settings for CouchDB
SERVER = 'http://admin:admin@localhost:5984'

# connecting CouchDB server
server = couchdb.Server(SERVER)

# longitude and latitude
MELBOURNE = [144.7, -38.1, 145.3, -37.5]
SYDNEY = [150.8, -34, 151.3, -33.6]


class MyStreamListener(tweepy.StreamListener):

    def on_connect(self):
        print('Connected to Twitter, start streaming...')

    def on_timeout(self):
        print('Stream connection times out.')

    def on_disconnect(self, notice):
        print('Disconnected: ', notice)

    def on_status(self, status):
        tweet_object = status._json

        try:
            coordinates = tweet_object['coordinates']['coordinates']
        except TypeError:
            return

        try:
            tweet = status.extended_tweet
            text = tweet['full_text']
        except AttributeError:
            text = status.text

        is_retweeted = False
        if 'retweeted_status' in tweet_object.keys():
            is_retweeted = True

        item = {
            '_id': tweet_object['id_str'],
            'text': text,
            'hashtags': methods.return_hashtags(tweet_object['entities']['hashtags']),
            'symbols': tweet_object['entities']['symbols'],
            'coordinates': coordinates,
            'place': tweet_object['place']['full_name'],
            'is_retweet': is_retweeted,
            'user_screen_name': tweet_object['user']['screen_name'],
            'user_id': tweet_object['user']['id_str'],
            'user_description': tweet_object['user']['description']
        }

        if item['is_retweet']:
            retweet_from = tweet_object['retweeted_status']['user']['screen_name']
            item['retweet_from'] = retweet_from

        # sentiment score and subjectivity of the tweet text
        sentiment, subjectivity = methods.sentiment_score(text)
        item['sentiment_score'] = sentiment
        item['subjectivity'] = subjectivity

        # datetime information
        week, month, day, created_time, year = methods.process_datetime(tweet_object['created_at'])
        item['week'] = week
        item['month'] = month
        item['day'] = day
        item['time'] = created_time
        item['year'] = year

        try:
            db.save(item)
            print('Inserted one.')
        except couchdb.http.ResourceConflict:
            print('Tweet already existed: ', status.id)
        except tweepy.RateLimitError:
            time.sleep(180)
        except tweepy.TweepError as e:
            print(str(e))


if __name__ == '__main__':
    options = methods.readCommand(sys.argv[1:])

    query = options.query
    database_name = options.database
    timeline_database = options.timeline
    user_database = options.userdb

    # connect to or create a database
    try:
        db = server[database_name]
    except couchdb.http.ResourceNotFound:
        db = server.create(database_name)

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    myStream.filter(locations=SYDNEY, is_async=True)

