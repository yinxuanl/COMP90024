from textblob import TextBlob


def return_hashtags(hashtags):
    if len(hashtags) == 0:
        return []
    return [tag['text'] for tag in hashtags]


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

    parser.add_option('-u', '--userdb', dest='userdb', help='user database', default='')

    options, otherjunk = parser.parse_args(argv)
    # assert len(otherjunk) == 0, "Unrecognized options: " + str(otherjunk)

    return options


def sentiment_score(string):
    score = TextBlob(string).sentiment
    return round(score.polarity, 2), round(score.subjectivity, 2)


# return: week, month, day, time, year
def process_datetime(datetime):
    items = datetime.split(' ')
    return items[0], items[1], items[2], items[3], items[5]


def process_tweet(tweet_object):
    is_retweeted = False
    if 'retweeted_status' in tweet_object.keys():
        is_retweeted = True

    item = {
        '_id': tweet_object['id_str'],
        'text': tweet_object['full_text'],
        'hashtags': return_hashtags(tweet_object['entities']['hashtags']),
        'symbols': tweet_object['entities']['symbols'],
        'user_screen_name': tweet_object['user']['screen_name'],
        'coordinates': tweet_object['coordinates']['coordinates'],
        'place': tweet_object['place']['full_name'],
        'is_retweet': is_retweeted

    }

    if item['is_retweet']:
        retweet_from = tweet_object['retweeted_status']['user']['screen_name']
        item['retweet_from'] = retweet_from

    # sentiment score and subjectivity of the tweet text
    sentiment, subjectivity = sentiment_score(item['text'])
    item['sentiment_score'] = sentiment
    item['subjectivity'] = subjectivity

    # datetime information
    week, month, day, created_time, year = process_datetime(tweet_object['created_at'])
    item['week'] = week
    item['month'] = month
    item['day'] = day
    item['time'] = created_time
    item['year'] = year
    return item


def process_user(user_object):
    item = {
        '_id': user_object['screen_name'],
        'name': user_object['name'],
        'id_str': user_object['id_str'],
        'location': user_object['location'],
        'description': user_object['description']
    }
    return item


def insert_new_view(new_view_name, new_view, database, design_document):
    design_name = '_design/' + design_document
    document = database[design_name]
    views = document['views']
    views[new_view_name] = new_view
    document['views'] = views
    database[document.id] = document

