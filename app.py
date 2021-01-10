import json
import numpy
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def start():
    '''
    run crunches
    '''
    tweets = parse('./data/tweet.js')
    #crunch_timeseries_counts(tweets)
    crunch_timeseries_sentiment(tweets)

def parse(path):
    '''
    get data
    '''
    f = open(path, "r", encoding="utf-8")
    jsoncontent = f.read()
    startidx = jsoncontent.index('=') + 1
    jsoncontent = jsoncontent[startidx:].strip()
    tweets = json.loads(jsoncontent)
    return [list(x.values())[0] for x in tweets]

def plot_timeseries_bar(xs,ys,title='Data'):
    _, ax = plt.subplots()
    ax.bar(xs,ys)
    ax.set_title(title)
    ax.legend()
    ax.set_xlabel('Date')
    axFormatDate(ax)
    ax.set_ylabel('Number')
    plt.show()

def axFormatDate(ax):
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.tick_params(axis='x', rotation=90)

def dayOfTweet(tweet,prop='created_at'):
    '''
    returns the date object of the tweet without time info
    '''
    return datetime.strptime(tweett[prop],'%a %b %d %H:%M:%S +0000 %Y').date()

def crunch_timeseries_counts(tweets):
    '''
    shows daily counts over time
    '''
    
    dates = [dayOfTweet(t) for t in tweets]
    unique, counts = numpy.unique(dates, return_counts=True)
    plot_timeseries_bar(unique,counts,'Tweets Per Day')

    #bonus: most popular days
    bins = list(zip(unique, counts))
    bins = sorted(bins, key=lambda x: x[1],reverse=True)[0:10]
    print('Your Most Active Days',bins)

def crunch_timeseries_sentiment(tweets):
    '''
    shows daily sentiment over time
    '''
    mytweets = [t for t in tweets if t['retweeted'] == False]
    mytweetsbyday = {}
    for t in mytweets:
        date = dayOfTweet(t)
        mytweetsbyday[date] = mytweetsbyday[date] if date in mytweetsbyday else []
        mytweetsbyday[date] = mytweetsbyday[date].append(t['full_text'])

    print(mytweetsbyday.entities()[0:10])

if __name__ == "__main__":
    start()