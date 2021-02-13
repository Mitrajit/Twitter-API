import sys, tweepy, geocoder
from playsound import playsound
from cryptography.fernet import Fernet
try :
    if sys.argv[1]=='-API'or sys.argv[1]=='-api':
        cred = [b'']*5
        cred[2]=Fernet.generate_key().decode("UTF-8")
        f=Fernet(cred[2])
        cred[0]=f.encrypt(bytes(sys.argv[2],'UTF-8')).decode()
        cred[1]=f.encrypt(bytes(sys.argv[3],'UTF-8')).decode("UTF-8")
        cred[3]=f.encrypt(bytes(sys.argv[4],'UTF-8')).decode("UTF-8")
        cred[4]=f.encrypt(bytes(sys.argv[5],'UTF-8')).decode("UTF-8")
        with open("cf.cfg","w") as wr:
            wr.write("\n".join(cred))
        print('API, tokens keys and secrets are saved')
        sys.exit(0)
    handler = open("cf.cfg","r")
    cred = handler.read().split()
    f = Fernet(cred[2].encode())
    auth = tweepy.OAuthHandler(f.decrypt(cred[0].encode()).decode(), f.decrypt(cred[1].encode()).decode())
    auth.set_access_token(f.decrypt(cred[3].encode()).decode(), f.decrypt(cred[4].encode()).decode())
    print("OAuthHandler set")
    api = tweepy.API(auth)
    print("logged in as @"+api.me().screen_name)
except tweepy.error.TweepError as tp:
    print("Could not log in with the given credentials\n",tp)
    sys.exit(0)
except IndexError as tw:
    print("tweet followed by Text in \"\" tweets from the account logged in\n-api <api key> <api secret> <token key> <token secret>-d\tdeletes the last tweet sent\n-tr\t shows trends of the region")
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
