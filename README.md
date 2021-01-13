# my-tweet-analysis
Parses the twitter tweet.js file and performs analysis on the dataset

# Requirements
1. [Python 3](https://www.python.org/downloads/release/python-391/)
1. A [Twitter Archive](https://help.twitter.com/en/managing-your-account/how-to-download-your-twitter-archive)
1. [pip](https://pip.pypa.io/en/stable/installing/)
1. With pip, install the app's dependencies:
```bash
#cd to this directory
pip install -r requirements.txt
```

# Usage
This application uses the paradigm of *crunches* which allow the user to selectively perform various "number crunching" algorithms on the dataset. The crunch name is a supplied argument under ```-c```. See below for examples.

### Graph of Counts Per Day
```bash
python my_tweet_analysis.py -f ./path/to/tweet.js -u whirledsol -c timeseries_counts
```

### Graph of Sentiment/Polarity in Tweets 
```bash
python my_tweet_analysis.py -f ./path/to/tweet.js -u whirledsol -c crunch_timeseries_sentiment
```

### Graph of Sentiment/Polarity in Tweets, averaged by Month
```bash
python my_tweet_analysis.py -f ./path/to/tweet.js -u whirledsol -c crunch_timeseries_sentiment_trend
```

### For more information...
```bash
python my_tweet_analysis.py -h
```
