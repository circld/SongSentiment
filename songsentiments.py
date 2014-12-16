"""
Main body of project:
    - calls to billboard.py
    - calls to lyrics.py
    - conducts analysis
    - builds visualizations
"""

import billboard.billboard as bb
from bs4 import BeautifulSoup
from lyrics import extract_lyrics


class EntrySentiment(bb.ChartEntry):

    def __init__(self, title, artist, peakPos, lastPos, weeks, rank, change):
        bb.ChartEntry.__init__(self, title, artist, peakPos, lastPos, weeks,
                               rank, change)
        self.lyrics = 'hi'  # extract_lyrics()
        self.sentiment = 0.0


class ChartSentiment(bb.ChartData):

    def __init__(self, name, date):
        bb.ChartData.__init__(self, name, date)

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

            self.entries.append(EntrySentiment(title, artist, peakPos, lastPos, weeks, rank, change))


# test case
def test_case():
    test = bb.ChartData('hot-100', '1980-09-27')
    return test.entries  # list of ChartEntry objs (.title, .artist, etc)


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
    from pandas import date_range

    # starting and ending Saturdays
    if start_date is None:
        start_date = date(1965, 1, 2)
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        start_date = start_date + timedelta(days=5 - start_date.weekday())
    if end_date is None:
        end_date = date.today()
    else:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    end_date = end_date - timedelta(days=(end_date.weekday() + 2) % 7)

    return date_range(start_date, end_date)

# TODO: complete extraction function to pull all rankings for each date
# >>> need to think about how to store data
def extract_billboard_rankings(datelist):
    pass
    # print str(saturdays()[0].date())

new = ChartSentiment('hot-100', '1980-09-20')

# TODO: complete lyric extraction over collection of songs