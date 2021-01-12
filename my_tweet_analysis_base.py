"""
my_tweet_analysis_base.py
common functions
@author: whirledsol
"""

import numpy,re
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from sentifish import Sentiment

def plot_timeseries(xs,ys,kind="plot",title='Data',yLabel='Number',cmap=None):
    _, ax = plt.subplots()

    color = 'k'
    if cmap is not None:
        color_scale = lambda y: (y - numpy.min(y)) / (numpy.max(y) - numpy.min(y))
        color = cmap(color_scale(ys))
    if kind == 'bar':
        ax.bar(xs,ys,color=color)
    else:
        ax.plot(xs, ys, '-o', color=color)

    ax.set_title(title)
    ax.legend()
    ax.set_xlabel('Date')
    axFormatDate(ax)
    ax.set_ylabel(yLabel)
    plt.show()

def axFormatDate(ax):
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.tick_params(axis='x', rotation=90)

def tweet_getDate(tweet,prop='created_at',dateOnly=False):
    '''
    returns the date object of the tweet without time info
    '''
    dt = datetime.strptime(tweet[prop],'%a %b %d %H:%M:%S +0000 %Y')
    if dateOnly:
        dt = dt.date()
    return dt

def tweet_ismine(tweet):
    '''
    cleans out tweets that aren't mine
    '''
    return tweet['retweeted'] == False and not tweet['full_text'].startswith('RT ')

def tweet_getText(tweet,clean=False):
    '''
    gets the tweet text
    '''
    text = tweet['full_text']
    if clean:
        text = re.sub(r'@(\w){1,15}','',text)
        text = re.sub(r'https?:\/\/[^\s]*','',text)
    return text

def calc_sentiments(tweets):
    '''
    creates list of list: [date,text,polarity]
    '''
    mysentiments = [t for t in tweets if tweet_ismine(t)]
    mysentiments = [[tweet_getDate(t),tweet_getText(t,True),0] for t in mysentiments]

    for i in range(len(mysentiments)):
        date,t,_ = mysentiments[i]
        try:
            polarity = Sentiment(t).analyze()
            mysentiments[i] = [date,t,polarity]
        except:
            print('could not analyize',t)

if __name__ == "__main__":
    start()