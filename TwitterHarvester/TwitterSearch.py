import sys
import re
import time
import couchdb
import tweepy
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
server = couchdb.Server(SERVER)

# geo information
CITY = '-33.865143,151.209900'  # sydney
RANGE = '30mi'
# CITY = '-23.322, 132.892'
# RANGE = '2000mi'

# time range information
FROM_DATE = '2019-05-08'
TO_DATE = '2019-05-15'


def search(query):
    # max_tweets = 5
    collection = tweepy.Cursor(
        api.search,
        q=query,
        tweet_mode='extended',
        since=FROM_DATE,
        until=TO_DATE,
        geocode=CITY + ',' + RANGE
    ).items()
    searched_tweets = [status for status in collection]
    print(len(searched_tweets))

    users = []  # save authors of all collected tweets

    for tweet in searched_tweets:

        tweet_object = tweet._json
        item = methods.process_tweet(tweet_object)

        try:
            db.save(item)
            # print('Inserted one tweet...')
        except couchdb.http.ResourceConflict:
            print('Tweet already existed.')

        # if this tweet is retweeted from other user, save the retweeted user for later crawling
        if 'retweet_from' in item.keys():
            retweet_user = methods.process_user(tweet_object['retweeted_status']['user'])
            users.append(retweet_user)

        # save the author for later crawling
        author = methods.process_user(tweet_object['user'])
        users.append(author)

    for user in users:

        try:
            user_db.save(user)

            screen_name = user['_id']
            timelines = [status for status in
                         tweepy.Cursor(
                             api.user_timeline,
                             screen_name=screen_name,
                             tweet_mode='extended',
                             include_rts=True,
                             count=2000
                         ).items()]

            print('Crawled one user, start saving.')

            for status in timelines:
                status_object = status._json
                timeline_item = {
                    '_id': status_object['id_str'],
                    'text': status_object['full_text'],
                    'user': status_object['user']['screen_name']
                }

                sentiment, subjectivity = methods.sentiment_score(timeline_item['text'])
                timeline_item['sentiment'] = sentiment
                timeline_item['subjectivity'] = subjectivity

                try:
                    udb.save(timeline_item)
                    # print('Inserted one timeline status...')
                except couchdb.http.ResourceConflict:
                    print('User status already existed.')
                except couchdb.ServerError as e:
                    print(str(e))

                # if the status contains key word, save it to related db
                quries = query.split(',')
                for q in quries:
                    # if the user timeline status contains any key words, save it to related database
                    if re.search(q, timeline_item['text']):
                        item = methods.process_tweet(status_object)
                        try:
                            db.save(item)
                        except couchdb.http.ResourceConflict:
                            print('Tweet already existed.')
                        break

        except couchdb.ServerError:
            print(couchdb.http.ServerError)
        except couchdb.http.ResourceConflict:
            print('User already existed.')
        except tweepy.error.RateLimitError as e:
            print(str(e))
            time.sleep(180)
        except tweepy.error.TweepError as e:
            print(str(e))
            time.sleep(180)


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

    # user home timeline database
    try:
        udb = server[timeline_database]
    except couchdb.http.ResourceNotFound:
        udb = server.create(timeline_database)

    # user database
    try:
        user_db = server[user_database]
    except couchdb.http.ResourceNotFound:
        user_db = server.create(user_database)

    search(query)
