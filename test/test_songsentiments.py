"""
Unit tests for songsentiments.py
"""

import songsentiments as ss


def test_case():
    assert type(ss.test_case()) == list


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


