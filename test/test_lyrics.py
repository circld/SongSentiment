"""
Unit tests for lyric.py
"""

import lyrics
import urllib2


class test_build_address(object):

    artist = 'olivia newton john/electric light orchestra'
    song = 'xanadu'
    address = lyrics.build_address(artist, song)

    def test_build_address_valid_url(self):
        assert urllib2.urlopen(self.address).getcode() == 200


def test_case_is_string():
    assert type(lyrics.test_case()) == str


def test_extract_lyrics():
    artist, song = 'duran duran', 'hungry like the wolf'
    assert type(lyrics.extract_lyrics(artist, song)) == str

