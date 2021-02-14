import sys, tweepy, geocoder
from playsound import playsound
import encryptdecrypt38
try :
    if sys.argv[1]=='-API'or sys.argv[1]=='-api':
        encryptdecrypt38.encrypt([sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5]])
        print('API, tokens keys and secrets are saved')
        sys.exit(0)
    cred=encryptdecrypt38.decrypt()
    auth = tweepy.OAuthHandler(cred[0], cred[1])
    auth.set_access_token(cred[2], cred[3])
    print("OAuthHandler set")
    api = tweepy.API(auth)
    print("logged in as @"+api.me().screen_name)
except tweepy.error.TweepError as tp:
    print("Could not log in with the given credentials\n",tp)
    sys.exit(0)
except IndexError as tw:
    print("tweet followed by Text in \"\" tweets from the account logged in\n-api <api key> <api secret> <token key> <token secret>\n-d\tdeletes the last tweet sent\n-tr\t shows trends of the region")
    sys.exit(0)
if sys.argv[1] == '-d' :
    tweet = api.user_timeline(count = 1)[0]
    print("Are you sure you want to delete this tweet(Y/N):\n",tweet.text.lstrip())
    confirm = input('')
    if confirm =='Y' or confirm == 'y':
        api.destroy_status(tweet.id)
        playsound('delete-tweet.mp3')
        print('Tweet is deleted')
    else:
        print('Tweet is not deleted')
elif sys.argv[1]=='-tr':
    loc = api.me().location
    print("Trending today for",loc)
    g = geocoder.osm(loc) # getting object that has location's latitude and longitude
    closest_loc = api.trends_closest(g.lat, g.lng)
    trends = api.trends_place(closest_loc[0]['woeid'])
    playsound('tweet-sfx.mp3')
    for trds in trends[0]['trends'][0:9] :
        print(trds['name']+"\t"+str(trds['tweet_volume']))
    # with open("twitter_{}_trend.json".format(loc),"w") as wp:
    #     wp.write(json.dumps(trends, indent=1))
    # print("Trending today for",loc)
    # with open("twitter_Kolkata_trend.json", 'r') as j:
    #     for trends in json.loads(j.read())[0]['trends'][0:9] :
    #         print(trends['name']+"\t"+str(trends['tweet_volume']))
else :
    api.update_status(status = sys.argv[1])
    playsound('tweet-sfx.mp3')
    print("Tweeted")
