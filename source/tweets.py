from twython import Twython, TwythonError

def getTweet(tweetId):
    # Credentials
    CONSUMER_KEY = "WKtmu8QRdyTtKDeMirpDW50zj"
    CONSUMER_SECRET = "G3pP3ZLJBcE7AHhiGAOsLPy06956oXUCbGstp0OIKM8EEH7312"
    OAUTH_TOKEN = "104997748-7cCdw06UzvQI86C5bHskKl90qCPJi3vfbRTEef68"
    OAUTH_TOKEN_SECRET = "ojBA7ZYhqrMrv6z0MqkonY74wOfQ9WZpNFloFgHykBib9"

    # Constructor
    twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    # Query
    tweet = twitter.show_status(id=tweetId, tweet_mode='extended')
    print(tweet)
    infoTweet = {}
    infoTweet['text'] = tweet['full_text']
    if infoTweet['text'][0] + infoTweet['text'][1] == "RT":
        infoTweet['rt_status'] = True
        infoTweet['text'] = tweet['retweeted_status']['full_text']
    else:
        infoTweet['rt_status'] = False
    infoTweet['date'] = tweet['created_at']
    infoTweet['username'] = tweet['user']['name']
    infoTweet['user_scree_name'] = "@" + tweet['user']['screen_name']
    return infoTweet

#getTweet("1035486425842626560")