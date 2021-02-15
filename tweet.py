import sys
import encryptdecrypt38
try:
    import tweepy, geocoder, argparse
    from playsound import playsound
    from tabulate import tabulate
except ModuleNotFoundError :
    print("Libraries could not be imported\nUse \"pip install -r requirements.txt\"")
    sys.exit(0)
def delete_tweet() :
    tweet = api.user_timeline(count = 1)[0]
    print("Are you sure you want to delete this tweet(Y/N):\n",tweet.text.lstrip())
    confirm = input('')
    if confirm =='Y' or confirm == 'y':
        api.destroy_status(tweet.id)
        playsound('delete-tweet.mp3')
        print('Tweet is deleted')
    else:
        print('Tweet is not deleted')
def show_trending() :
    loc = api.me().location if len(args.tr)==0 else " ".join(args.tr)
    g = geocoder.osm(loc) # getting object that has location's latitude and longitude
    try :
        closest_loc = api.trends_closest(g.lat, g.lng)
        trends = api.trends_place(closest_loc[0]['woeid'])[0]['trends'][0:9]
    except tweepy.error.TweepError as te:
        print("Invalid cordinates",te,sep="\n")
        sys.exit(1)
    print("Trending today for",loc)
    playsound('tweet-sfx.mp3')
    print(tabulate([[trds['name'],trds['tweet_volume'],trds['url']]for trds in trends],headers=["Name","No. of tweets","URL"]))
    # with open("twitter_{}_trend.json".format(loc),"w") as wp:
    #     wp.write(json.dumps(trends, indent=1))
    # print("Trending today for",loc)
    # with open("twitter_Kolkata_trend.json", 'r') as j:
    #     for trends in json.loads(j.read())[0]['trends'][0:9] :
    #         print(trends['name']+"\t"+str(trends['tweet_volume']))
my_parser = argparse.ArgumentParser(description='List the content of a folder')
my_parser.add_argument('tweet',
                       metavar='tweet',
                       type=str,
                       action="append",
                       nargs="*",
                       help='tweet <The text you want to tweet>')
my_parser.add_argument('-api',
                       type=str,
                       metavar=("<api key>", "<api secret>" , "<token key>","<token secret>"),
                       action="store",
                       help='gets the api keys and secrets',
                       nargs=4)
my_parser.add_argument('-tr',
                       type=str,
                       metavar=("place name or global"),
                       action="store",
                       help='gets the trending in the given place',
                       nargs="*")
my_parser.add_argument('-d',
                       action="store_true",
                       help='deletes the last tweet')
args = my_parser.parse_args()
if len(args.tweet[0])==0 and args.api is None and not args.d and args.tr is None:
    my_parser.print_help()
    sys.exit(0)
try :
    if args.api is not None:
        encryptdecrypt38.encrypt([args.api[0],args.api[1],args.api[2],args.api[3]])
        print('API, tokens keys and secrets are saved')
    cred=encryptdecrypt38.decrypt()
    auth = tweepy.OAuthHandler(cred[0], cred[1])
    auth.set_access_token(cred[2], cred[3])
    print("OAuthHandler set")
    api = tweepy.API(auth)
    print("logged in as @"+api.me().screen_name)
except tweepy.error.TweepError as tp:
    print("Could not log in with the given credentials\n",tp)
    sys.exit(0)
except IndexError:
    my_parser.print_help()
    sys.exit(0)
if args.d :
    delete_tweet()
elif args.tr != None:
    show_trending()
elif len(args.tweet[0])!=0 :
    api.update_status(status = " ".join(args.tweet[0]))
    playsound('tweet-sfx.mp3')
    print("Tweeted")
