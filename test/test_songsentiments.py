"""
Unit tests for songsentiments.py
"""

import songsentiments as ss
from datetime import datetime


def test_case():
    assert type(ss.test_case()) == list


class test_EntrySentiment(object):

    real_song = ss.EntrySentiment('hotel california', 'eagles', 5, 11, 3, 12, -1)
    fake_song = ss.EntrySentiment('hotel alabama', 'eagles', 5, 11, 3, 12, -1)

    def test_instantiation(self):
        from billboard.billboard import ChartEntry
        assert issubclass(ss.EntrySentiment, ChartEntry)

    def test_instance_vars(self):
        assert (self.real_song.title == 'hotel california' and
                self.real_song.artist == 'eagles' and
                self.real_song.peakPos == 5)

    def test_lyrics_is_string(self):
        assert type(self.real_song.lyrics) is str

    def test_lyrics_download_success(self):
        assert self.real_song.success

    def test_lyrics_download_failure(self):
        assert not self.fake_song.success

    def test_fail_message(self):
        assert self.fake_song.lyrics[:7] == 'http://'


class test_ChartSentiment(object):

    weekly_data = ss.ChartSentiment('hot-100', '1980-09-27')

    def test_subclass_ChartData(self):
        from billboard.billboard import ChartData
        assert issubclass(ss.ChartSentiment, ChartData)

    def test_instantiation_entries(self):
        assert self.weekly_data.entries[0] is not None

    def test_all_lyrics(self):
        assert len(self.weekly_data.all_lyrics) > 10000

    def test_no_lyrics(self):
        assert type(self.weekly_data.no_lyrics) is list


class test_SongData(object):

    song = ss.SongData()
    song.add_song('Santana', 'Smooth', 'blah blah', 0.1142)

    def test_has_song(self):
        assert self.song.has_song('Santana', 'Smooth')

    def test_not_have_song(self):
        assert not self.song.has_song('Billy Joel', 'Piano Man')

    def test_access_data(self):
        assert self.song.get_sentiment('Santana', 'Smooth') == 0.1142



class test_saturdays(object):

    fmt = '%Y-%m-%d'

    def test_return_iterable(self):
        assert (i for i in ss.saturdays())

    def test_non_empty(self):
        assert len(ss.saturdays()) > 0

    def test_startdate_is_saturday(self):
        assert datetime.strptime(ss.saturdays()[0],
                                 self.fmt).weekday() == 5

    def test_enddate_is_saturday(self):
        assert datetime.strptime(ss.saturdays()[-1],
                                 self.fmt).weekday() == 5

    def test_usr_startdate_converts_to_saturday(self):
        this_day = ss.saturdays('1990-05-16')[0]
        assert datetime.strptime(this_day, self.fmt).weekday() == 5

    def test_usr_enddate_converts_to_saturday(self):
        this_day = ss.saturdays(end_date='1976-09-19')[-1]
        assert datetime.strptime(this_day, self.fmt).weekday() == 5


class test_extract_billboard_rankings(object):

    charts = ss.extract_billboard_rankings('1980-01-01', '1980-01-15')

    def test_returns_tuple(self):
        assert type(self.charts) is tuple

    def test_ChartSentiment_elements(self):
        assert self.charts[0].name == 'hot-100' and \
               self.charts[1].date == '1980-01-12'

    def test_length(self):
        assert len(self.charts) == 2
