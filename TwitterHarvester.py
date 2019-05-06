import couchdb
import tweepy
import sys
import json

# settings for Twitter API authentication
CONSUMER_KEY = 'R8Huo0RRHNfcGaXbEcWfKHjmg'
CONSUMER_SECRET = 'OFvsIk4SeLvLk3YhfZiieLumhteu9javO4DTsLJwUdJSd2OBBg'
ACCESS_TOKEN = '942702516805943296-CY5fdJ5N5UZ3FiLGIlj0b9U0jH39ak2'
ACCESS_TOKEN_SECRET = '2yK7u81Ia4NbWtR21GtQ1lJyKwxfqTDIO332Q6NGRlOUA'

# settings for CouchDB
# SERVER = 'http://admin:admin@103.6.254.11:5984/'
SERVER = 'http://127.0.0.1:5984/'
DATABASE = 'test'

# longitude and latitude
MELBOURNE = [144.7, -38.1, 145.3, -37.5]
SYDNEY = [150.8, -34, 151.3, -33.6]

# authentication for Twitter API
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# connecting CouchDB server
server = couchdb.Server(SERVER)

try:
    db = server[DATABASE]
except couchdb.http.ResourceNotFound:
    db = server.create(DATABASE)


def readCommand(argv):
    from optparse import OptionParser
    usage_str = """
    USAGE: python harvest.py <option>
    EXAMPLES: 
    """
    parser = OptionParser(usage_str)

    parser.add_option('-t', '--track', dest='track', help='enter query', default='')

    parser.add_option('-f', '--follow', dest='follow', help='follow', default='')

    parser.add_option('-c', '--city', dest='city', help='Melbourne or Sydney', default='Melbourne')

    options, otherjunk = parser.parse_args(argv)
    # assert len(otherjunk) == 0, "Unrecognized options: " + str(otherjunk)

    return options


class MyStreamListener(tweepy.StreamListener):

    # attributes saved: Tweet ID, User ID, created date, (longitude, latitude), text or full_text, hashtags
    def on_status(self, status):
        try:
            tweet = status.extended_tweet
            text = tweet['full_text']
            entities = tweet['entities']

            location = status.place.name
            bounding_box = status.place.bounding_box.coordinates

        except AttributeError:
            text = status.text
            entities = status.entities
            location = None
            bounding_box = None

        hashtags = entities['hashtags']
        usr_mentions = entities['user_mentions']
        symbols = entities['symbols']

        try:
            media = entities['media']
        except KeyError:
            media = None

        user_id = status.author.id
        user_location = status.author.location
        user_description = status.author.description

        coordinates = status.coordinates # could be None

        created_at = str(status.created_at)

        item = {
            '_id': str(status.id),
            'created_at': str(created_at),
            'text': text,
            'hashtags': hashtags,
            'user_mentioned': usr_mentions,
            'symbols': symbols,
            'media': media,
            'coordinates': coordinates,
            'location': location,
            'bounding_box': bounding_box,
            'user_id': user_id,
            'user_location': user_location,
            'user_description': user_description

        }

        try:
            db.save(item)
            print('Inserted one...')
        except couchdb.http.ResourceConflict:
            print('Tweet already existed: ', status.id)


if __name__ == '__main__':
    print('start streaming')
    options = readCommand(sys.argv[1:])

    track = options.track
    follow = options.follow
    city = options.city

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    if city == 'Melbourne':
        myStream.filter(track=[track], follow=[follow], locations=MELBOURNE, is_async=True)
    elif city == 'Sydney':
        myStream.filter(track=[track], follow=[follow], locations=SYDNEY, is_async=True)
    else:
        myStream.filter(track=[track], follow=[follow], is_async=True)
