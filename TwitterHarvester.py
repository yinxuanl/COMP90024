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
SERVER = 'http://admin:admin@103.6.254.11:5984/'
# SERVER = 'http://127.0.0.1:5984/'
DATABASE = 'history'


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

    parser.add_option('-a', '--locationa', dest='locationa', help='location', default='')

    parser.add_option('-b', '--locationb', dest='locationb', help='location', default='')

    parser.add_option('-c', '--locationc', dest='locationc', help='location', default='')

    parser.add_option('-d', '--locationd', dest='locationd', help='location', default='')

    options, otherjunk = parser.parse_args(argv)
    # assert len(otherjunk) == 0, "Unrecognized options: " + str(otherjunk)

    return options


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        # todo: interact with couchdb
        text = ''
        json_file = status._json

        if 'extended_tweet' in json_file.keys():
            text = json_file['extended_tweet']['full_text']
        else:
            text = status.text

        date = str(status.created_at)

        user_id = status.user.id

        hashtags = {}
        if 'hashtags' in json_file['entities'].keys():
            hashtags = dict(json_file['entities']['hashtags'])

        item = {'_id': str(status.id),'date':date, 'text': text, 'user_id': user_id, 'hashtags': hashtags}

        try:
            db.save(item)
            print('Inserted one...')
        except couchdb.http.ResourceConflict:
            print('Tweet already existed: ', status.id)


# todo: determine longitude and latitude for melbourne
# myStream.filter(locations=[144.7,-37.95,145.3,-37.65])


if __name__ == '__main__':
    print('start streaming')
    options = readCommand(sys.argv[1:])

    track = options.track
    follow = options.follow
    a = float(options.locationa)
    b = float(options.locationb)
    c = float(options.locationc)
    d = float(options.locationd)

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    if a is not None:
        myStream.filter(track=[track], follow=[follow], locations=[a,b,c,d], is_async=True)
    else:
        myStream.filter(track=[options.track], follow=[follow], is_async=True)
