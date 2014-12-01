"""
Main body of project:
    - calls to billboard.py
    - calls to lyrics.py
    - conducts analysis
    - builds visualizations
"""

import billboard.billboard as bb

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
    end_date = end_date - timedelta(days=end_date.weekday() % 5)

    return date_range(start_date, end_date)

# TODO: complete extraction function to pull all rankings for each date
# >>> need to think about how to store data
def extract_billboard_rankings(datelist):
    pass
    # print str(saturdays()[0].date())

# TODO: complete lyric extration over collection of songs