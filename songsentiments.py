"""
This module allows the downloading and visualization of Billboard Hot-100
songs. Sentiment scores are produced using AlchemyAPI
(http://www.alchemyapi.com/api/calling-the-api/).
"""

import billboard.billboard as bb
from bs4 import BeautifulSoup
from lyrics import extract_lyrics
from alchemyapi.alchemyapi import AlchemyAPI
import re
import pickle


class SongData(object):

    def __init__(self):
        self.data = dict()

    def has_song(self, artist, title):
        return (artist + title) in self.data.keys()

    def add_song(self, artist, title, lyrics, sentiment):
        self.data[artist+title] = dict()
        self.data[artist+title]['lyrics'] = lyrics
        self.data[artist+title]['sentiment'] = sentiment

    def get_lyrics(self, artist, title):
        return self.data[artist+title]['lyrics']

    def get_sentiment(self, artist, title):
        return self.data[artist+title]['sentiment']

    def has_lyrics(self, artist, title):
        return self.data[artist+title]['lyrics'][:7] != 'http://'


class EntrySentiment(bb.ChartEntry):

    store = SongData()
    counter = 0

    def __init__(self, title, artist, peakPos, lastPos, weeks, rank, change):
        bb.ChartEntry.__init__(self, title, artist, peakPos, lastPos, weeks,
                               rank, change)
        if not self.store.has_song(self.artist, self.title):
            lyrics = extract_lyrics(self.artist, self.title)
            self.success = lyrics[:7] != 'http://'
            sentiment = self.success and extract_sentiment(lyrics) or 0.0
            self.store.add_song(self.artist, self.title, lyrics, sentiment)
            if self.success:
                self.increment_counter()
        else:
            self.success = self.store.has_lyrics(self.artist, self.title)

    def get_lyrics(self):
        return self.store.get_lyrics(self.artist, self.title)

    def get_sentiment(self):
        return self.store.get_sentiment(self.artist, self.title)

    @classmethod
    def get_counter(self):
        return self.counter

    @classmethod
    def reset_counter(cls):
        cls.counter = 0

    @classmethod
    def increment_counter(cls):
        cls.counter += 1


class ChartSentiment(bb.ChartData):

    def __init__(self, date, limit=1000, name='hot-100'):
        self.limit = limit
        self.complete = None
        bb.ChartData.__init__(self, name, date)
        if self.complete is None:
           self.complete = True
        self.no_lyrics = [(i.artist, i.title, i.get_lyrics())
                          for i in self.entries if not i.success]
        sent_list = [j.get_sentiment() for j in self.entries if j.success]
        if len(sent_list) > 0:
            self.sentiment = sum(sent_list) / len(sent_list)
        else:
            self.sentiment = 0.0


    def fetchEntries(self, all=False):
        if self.latest:
            url = 'http://www.billboard.com/charts/%s' % (self.name)
        else:
            url = 'http://www.billboard.com/charts/%s/%s' % (self.name, self.date)

        html = bb.downloadHTML(url)
        soup = BeautifulSoup(html)

        for entry_soup in soup.find_all('article', {"class": "chart-row"}):

            # Grab title and artist
            basicInfoSoup = entry_soup.find('div', 'row-title').contents
            title = basicInfoSoup[1].string.strip()

            if (basicInfoSoup[3].find('a')):
                artist = basicInfoSoup[3].a.string.strip()
            else:
                artist = basicInfoSoup[3].string.strip()

            # Grab week data (peak rank, last week's rank, total weeks on chart)
            weekInfoSoup = entry_soup.find('div', 'stats').contents
            peakPos = int(weekInfoSoup[3].find('span', 'value').string.strip())

            lastPos = weekInfoSoup[1].find('span', 'value').string.strip()
            lastPos = 0 if lastPos == '--' else int(lastPos)

            weeks = int(weekInfoSoup[5].find('span', 'value').string.strip())

            # Get current rank
            rank = int(entry_soup.find('div', 'row-rank').find('span', 'this-week').string.strip())

            change = lastPos - rank
            if lastPos == 0:
                # New entry
                if weeks > 1:
                    # If entry has been on charts before, it's a re-entry
                    change = "Re-Entry"
                else:
                    change = "New"
            elif change > 0:
                change = "+" + str(change)
            else:
                change = str(change)

            if EntrySentiment.get_counter() < self.limit:
                self.entries.append(EntrySentiment(title, artist, peakPos, lastPos,
                                               weeks, rank, change))
            else:
                args = {'title': title, 'artist': artist,
                        'rank': rank, 'date': self.date}
                print("".join(['Reached limit. Did not add {title} by {artist}',
                               ' (#{rank}) in week {date}.']
                              ).format(**args))
                self.complete = False
                break


def saturdays(start_date=None, end_date=None):
    """
    Note: dates should be 'yyyy-mm-dd' format
    :param start_date: optional start date first saturday date returned will
      be this date if a Saturday or the next Saturday otherwise.
    :param end_date: optional end date, inclusive. Will return Saturday dates
      up to the most recent Saturday.
    :return: list of datetime objects for every Saturday between start_date
      and end_date, from start_date to today, or every Saturday between 1965
      and today (if neither argument is specified).
    """
    from datetime import date, datetime, timedelta
    from pandas import date_range, DateOffset

    # starting and ending Saturdays
    if start_date is None:
        start_date = date(1965, 1, 2)
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        start_date = start_date + timedelta(days=(5 - start_date.weekday()) % 7)
    if end_date is None:
        end_date = date.today()
    else:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    end_date = end_date - timedelta(days=(end_date.weekday() + 2) % 7)

    return [str(i.date()) for i in date_range(start_date, end_date,
                                              freq=DateOffset(days=7))]


def extract_sentiment(lyrics):
    alchemy = AlchemyAPI()
    response = alchemy.sentiment('text', lyrics)
    if 'docSentiment' not in response.keys():
        return 0.0
    if 'score' in response['docSentiment'].keys():
        return float(response['docSentiment']['score'])
    return 0.0


def extract_billboard_rankings(start=None, end=None, limit=1000):
    EntrySentiment.reset_counter()
    date_list = saturdays(start, end)
    chart_list = tuple()
    for week in date_list:
        print 'Processing ' + week + '...',
        chart_list += (ChartSentiment(week, limit),)
        print ' Complete'
    return chart_list


def pickle_charts(start, end, limit=1000):
    charts = extract_billboard_rankings(start, end, limit)
    full_charts = [ch for ch in charts if ch.complete]
    start_date = re.subn('-', '', full_charts[0].date)[0]
    end_date = re.subn('-', '', full_charts[-1].date)[0]
    new_name = '_'.join(['charts', start_date, end_date])
    pickle.dump(full_charts, open(new_name +'.p', 'wb'))
    return full_charts


def unpickle_charts():
    import glob
    import os
    pattern = 'charts_[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]_' + \
              '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9].p'
    to_load = glob.glob1(os.getcwd(), pattern)
    charts = list()
    for f in to_load:
        charts.extend(pickle.load(open(f, 'rb')))
    return charts


def visualize(chart_list):
    import matplotlib.pyplot as plt
    import math
    week = [i.date for i in chart_list]
    sent = [i.sentiment for i in chart_list]
    missing = [len(i.no_lyrics) for i in chart_list]
    n = len(week)
    wk_num = xrange(n)
    bar_width = 0.2 * math.e**n / (math.e**n + 10) + 0.2

    # create figure
    fig, ax1 = plt.subplots()
    ax1.plot(wk_num, sent, '-', color='navy')
    ax1.set_xlabel('Week')
    ax1.set_ylabel('Mean sentiment (navy)')
    plt.xticks((wk_num[0], wk_num[n/4], wk_num[n/2], wk_num[n*3/4], wk_num[-1]),
               (week[0], week[n/4], week[n/2], week[n*3/4], week[-1]))
    ax1.set_title(''.join(['Billboard Hot 100 mean sentiment by week\n',
                           '({fr} to {to})']).format(fr=week[0], to=week[-1]),
                  fontdict={'fontsize': 12})
    ax2 = ax1.twinx()
    ax2.bar(wk_num, missing, width=bar_width, color='orange', alpha=.5,
            align='center')
    ax2.set_ylabel('# missing lyrics (orange)')
    ax2.set_ylim(top=4 * max(missing))
    plt.show()


def check_prompt(string):
    from os import _exit
    from datetime import date
    pattern = re.compile('([qQ](uit)?|[eE]xit)')
    if string == '':
        return True
    elif re.search(pattern, string):
        print('Exiting program.')
        _exit(1)
    elif re.match('\d{4}-\d{2}-\d{2}', string):
        if string < '1960-01-02' or string > str(date.today):
            print('Invalid date. Must be between 1960-01-02 and today.')
            return False
        return True
    else:
        print('Invalid entry. Please try again (q to quit).')
        return False


def main():

    # visualize data previously downloaded
    charts = unpickle_charts()
    visualize(charts)

    # user selects date range to download & visualize
    print('Specify your own date ranges to visualize.\n')
    print(''.join(['Instructions: you will be prompted to enter a start ',
                   'and end dates. Leaving the start date blank will start',
                   ' the visualization from 1960-01-02, while leaving the',
                   ' end date blank sets the end date to today.\n',
                   'As a single week may take a up to a minute to process,',
                   ' please be conservative with the length of the date ',
                   'range you select.\n\nenter q (Q, quit, exit) at either ',
                   'prompt to exit']))

    okay = False
    while not okay:
        start = raw_input('Select start date (yyyy-mm-dd):\n>> ')
        okay = check_prompt(start)
    okay = False
    while not okay:
        end = raw_input('Select end date (yyyy-mm-dd):\n>> ')
        okay = check_prompt(end)
    if start == '':
        start = None
    if end == '':
        end = None
    save_it = raw_input('Enter Y to save data to current working directory.\n>> ')

    print(''.join(['Please note that under a free account, you are limited ',
                   'to 1,000 Alchemy API calls per day; this may result in',
                   ' the plotted date range being smaller than what you ',
                   'had selected above.\n\n']))
    if save_it in ('y', 'Y', 'yes', 'Yes'):
        new_data = pickle_charts(start, end)
    else:
        new_data = extract_billboard_rankings(start, end)
    visualize(new_data)


if __name__ == '__main__':

    main()

