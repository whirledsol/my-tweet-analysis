import json,numpy,nltk,re
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from sentifish import Sentiment

def start():
    '''
    run crunches
    '''
    tweets = parse('./data/tweet.js')
    username = 'whirledsol'
    #crunch_timeseries_counts(tweets,username)
    crunch_timeseries_sentiment(tweets,username)

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
    shows daily sentiment over time
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
        
    #bar chart
    xs = [i[0] for i in mysentiments]
    ys = [i[2] for i in mysentiments]
    title = f"@{username}'s Tweet Sentiments"
    cmap = plt.get_cmap("RdYlGn")
    plot_timeseries(xs, ys, title=title, kind="bar", yLabel='Positivity', cmap=cmap)

    #monthly trend chart
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


    #bonus: most negative tweets
    #neg = sorted(mysentiments, key=lambda x: x[2],reverse=False)[0:10]
    #print('Your Most Negative Tweet',neg)
    
if __name__ == "__main__":
    start()