import json
import numpy
from datetime import datetime

def start():
    '''
    run crunches
    '''
    tweets = parse('./data/tweet.js')
    print(tweets)
    crunch_timeseries_counts(tweets)


def parse(path):
    '''
    get data
    '''
    f = open(path, "r")
    jsoncontent = f.read()
    tweets = json.loads(jsoncontent)
    return tweets
    
def crunch_timeseries_counts(tweets):
    '''
    shows daily counts over time
    '''
    xs=[]
    ys=[]
    for tweet in tweets:
        pass



if __name__ == "__main__":
    start()