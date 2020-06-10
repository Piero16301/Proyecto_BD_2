from twython import Twython, TwythonError

def getTextTweet(tweetId):
    # Credentials
    CONSUMER_KEY = "WKtmu8QRdyTtKDeMirpDW50zj"
    CONSUMER_SECRET = "G3pP3ZLJBcE7AHhiGAOsLPy06956oXUCbGstp0OIKM8EEH7312"
    OAUTH_TOKEN = "104997748-7cCdw06UzvQI86C5bHskKl90qCPJi3vfbRTEef68"
    OAUTH_TOKEN_SECRET = "ojBA7ZYhqrMrv6z0MqkonY74wOfQ9WZpNFloFgHykBib9"

    # Constructor
    twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    # Query
    tweet = twitter.show_status(id=tweetId, tweet_mode='extended')
    infoTweet = {}
    infoTweet['rt_status'] = tweet['retweeted_status'] is not None
    if infoTweet['rt_status']:
        infoTweet['text'] = tweet['retweeted_status']['full_text']
        infoTweet['name'] = tweet['entities']['user_mentions'][0]['name']
        infoTweet['screen_name'] = tweet['entities']['user_mentions'][0]['screen_name']
    else:
        infoTweet['text'] = tweet['full_text']
    infoTweet['date'] = tweet['created_at']
    infoTweet['username'] = tweet['user']['name']
    infoTweet['user_scree_name'] = "@" + tweet['user']['screen_name']
    return infoTweet


print(getTextTweet('1026814183042686976'))
