"""
Unit tests for songsentiments.py
"""

import songsentiments as ss


def test_case():
    assert type(ss.test_case()) == list


class test_EntrySentiment(object):

    sent_entry = ss.EntrySentiment('title', 'artist', 5, 11, 3, 12, -1)

    def test_instantiation(self):
        from billboard.billboard import ChartEntry
        assert issubclass(ss.EntrySentiment, ChartEntry)

    def test_instance_vars(self):
        assert (self.sent_entry.title == 'title' and
                self.sent_entry.artist == 'artist' and
                self.sent_entry.peakPos == 5)

    def test_lyrics_is_string(self):
        assert type(self.sent_entry.lyrics) is str

    def test_sentiment_is_float(self):
        assert type(self.sent_entry.sentiment) is float



class test_ChartSentiment(object):

    def test_subclass_ChartData(self):
        from billboard.billboard import ChartData
        assert issubclass(ss.ChartSentiment, ChartData)

    def test_instantiation_entries(self):
        weekly_data = ss.ChartSentiment('hot-100', '1980-09-27')
        assert weekly_data.entries[0] is not None



class test_saturdays(object):

    def test_return_iterable(self):
        assert (i for i in ss.saturdays())

    def test_non_empty(self):
        assert len(ss.saturdays()) > 0

    def test_startdate_is_saturday(self):
        assert ss.saturdays()[0].weekday() == 5

    def test_enddate_is_saturday(self):
        assert ss.saturdays()[-1].weekday() == 5

    def test_usr_startdate_converts_to_saturday(self):
        assert ss.saturdays('1990-05-16')[0].weekday() == 5

    def test_usr_enddate_converts_to_saturday(self):
        assert ss.saturdays(end_date='1976-09-19')[-1].weekday() == 5


