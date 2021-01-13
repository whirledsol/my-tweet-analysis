"""
my_tweet_analysis.py
driver
@author: whirledsol
"""

import json,argparse
from my_tweet_analysis_base import *
from my_tweet_analysis_crunches import my_tweet_analysis_crunches

def start():
    '''
    run crunches
    '''
    args = parse()
    tweets = load(args.file)

    crunchname = f"crunch_{args.crunch}"
    crunch = None
    
    try:
        crunch = getattr(my_tweet_analysis_crunches, crunchname)
    except:
        print('Could not find the appropriate crunch to call',crunchname)
        exit()

    crunch(tweets,args.username)
    
def parse():
    '''
    sets the args needed to run and returns them
    '''
    #default path
    default_file = './data/tweet.js'

    #exposed crunches
    crunches = ['timeseries_counts','timeseries_sentiment','timeseries_sentiment_trend']

    parser = argparse.ArgumentParser(description='Run analytics on twitter archive data.')
    parser.add_argument('-f','--file',dest='file',type=str, default=default_file, help=f"path to tweet.js file, by default looks for {default_file}")
    parser.add_argument('-u','--username',dest='username',type=str, help='your username, for display only', required=True)
    parser.add_argument('-c','--crunch',dest='crunch',type=str, help='the type of analysis to perform', required=True, choices=crunches)

    args = parser.parse_args()

    #cleanup
    args.username = args.username.strip('@')
    return args


def load(path):
    '''
    get data
    '''
    f = open(path, "r", encoding="utf-8")
    jsoncontent = f.read()
    startidx = jsoncontent.index('=') + 1
    jsoncontent = jsoncontent[startidx:].strip()
    tweets = json.loads(jsoncontent)
    return [list(x.values())[0] for x in tweets]

if __name__ == "__main__":
    start()