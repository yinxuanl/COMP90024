import sys

import couchdb
import tweepy

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
# ssh -i dbServer.key -L 7001:localhost:5984 ubuntu@172.26.38.166
# SERVER = 'http://admin:admin@172.26.38.166:5984/'
SERVER = 'http://127.0.0.1:5984/'
server = couchdb.Server(SERVER)
try:
    user_db = server['twitter_user']
except couchdb.http.ResourceNotFound:
    user_db = server.create('twitter_user')

def readCommand(argv):
    from optparse import OptionParser
    usage_str = """
    USAGE: python harvest.py <option>
    EXAMPLES: 
    """
    parser = OptionParser(usage_str)

    parser.add_option('-q', '--query', dest='query', help='enter query', default='')

    parser.add_option('-d', '--database', dest='database', help='database name', default='')

    parser.add_option('-t', '--timeline', dest='timeline', help='home timeline', default='')

    options, otherjunk = parser.parse_args(argv)
    # assert len(otherjunk) == 0, "Unrecognized options: " + str(otherjunk)

    return options


def search(query):
    max_tweets = 5
    collection = tweepy.Cursor(
        api.search,
        q=query,
        tweet_mode='extended',
        since='2019-05-01',
        until='2019-05-08',
        geocode='-33.865143,151.209900,15mi'
    ).items(max_tweets)
    searched_tweets = [status for status in collection]

    users = []

    for tweet in searched_tweets:
        tweet_object = tweet._json
        item = {
            '_id': tweet_object['id_str'],
            'text': tweet_object['full_text'],
            'hashtags': tweet_object['entities']['hashtags'],
            'symbols': tweet_object['entities']['symbols'],
            'user_id': tweet_object['user']['id_str'],
            'geo': tweet_object['geo'],
            'coordinates': tweet_object['coordinates'],
            'place': tweet_object['place'],
            'is_retweet': tweet_object['retweeted']
        }
        try:
            db.save(item)
            print('Inserted one tweet...')
        except couchdb.http.ResourceConflict:
            print('Tweet already existed.')

        user = {
            '_id': item['user_id'],
            'user name': tweet_object['user']['name'],
            'user description': tweet_object['user']['description']
        }

        users.append(tweet_object['user']['id'])  # number, not string

        try:
            user_db.save(user)
            print('Inserted one user...')
        except couchdb.http.ResourceConflict:
            print('User already existed.')

    for user in users:
        timelines = [status for status in tweepy.Cursor(api.user_timeline, user_id=user, tweet_mode='extended').items()]

        for status in timelines:
            tweet_object = status._json
            timeline_item = {
                '_id': tweet_object['id_str'],
                'text': tweet_object['full_text'],
                'user_id': tweet_object['user']['id_str']
            }

            try:
                udb.save(timeline_item)
                print('Inserted one timeline status...')
            except couchdb.http.ResourceConflict:
                print('User status already existed.')


if __name__ == '__main__':
    options = readCommand(sys.argv[1:])

    query = options.query
    database_name = options.database
    timeline_database = options.timeline

    # connect to or create a database
    try:
        db = server[database_name]
    except couchdb.http.ResourceNotFound:
        db = server.create(database_name)

    try:
        udb = server[timeline_database]
    except couchdb.http.ResourceNotFound:
        udb = server.create(timeline_database)

    search(query)
