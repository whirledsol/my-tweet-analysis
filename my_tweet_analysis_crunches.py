"""
my_tweet_analysis_crunches.py
quick crunches of the data
@author: whirledsol
"""

import numpy
from datetime import datetime
from my_tweet_analysis_base import *

def crunch_timeseries_counts(tweets,username):
    '''
    shows daily counts over time
    '''
    
    dates = [tweet_getDate(t, True) for t in tweets]
    unique, counts = numpy.unique(dates, return_counts=True)
    plot_timeseries(unique,counts,kind='bar',title=f"@{username}'s Tweet Count Per Day")

    #bonus: most popular days
    top = list(zip(unique, counts))
    top = sorted(top, key=lambda x: x[1],reverse=True)[0:10]
    print('Your Most Active Days',top)

def crunch_timeseries_sentiment(tweets,username):
    '''
    shows daily sentiment over time as bar chart
    '''
    mysentiments = calc_sentiments(tweets)
        
    xs = [i[0] for i in mysentiments]
    ys = [i[2] for i in mysentiments]
    title = f"@{username}'s Tweet Sentiments"
    cmap = plt.get_cmap("RdYlGn")
    plot_timeseries(xs, ys, title=title, kind="bar", yLabel='Positivity', cmap=cmap)

    #bonus: most negative tweets
    #neg = sorted(mysentiments, key=lambda x: x[2],reverse=False)[0:10]
    #print('Your Most Negative Tweet',neg)
    
def crunch_timeseries_sentiment_trend(tweets,username):
    '''
    shows monthly avg sentiments as line chart
    '''
    mysentiments = calc_sentiments(tweets)

    trend = {} #month:numpy.mean(polarity)
    for date,tweet,polarity in mysentiments:
        month = datetime.strptime(date.strftime('%m-%y'),'%m-%y')
        trend[month] = trend[month] + [polarity] if month in trend else [polarity]
    trend = [[month,numpy.mean(polarities)] for month,polarities in trend.items()]
    trend = sorted(trend, key=lambda x: x[0])
    xs = [i[0] for i in trend]
    ys = [i[1] for i in trend]
    title  = f"@{username}'s Tweet Sentiment Trend"
    plot_timeseries(xs, ys, title=title, yLabel='Positivity')

