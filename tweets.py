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
    tweet = twitter.show_status(id="1026814183042686976", tweet_mode='extended')
    if tweet['retweeted_status'] is not None:
        return tweet['retweeted_status']['full_text']
    else:
        return tweet['full_text']
