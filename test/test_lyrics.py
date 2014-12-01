"""
Unit tests for lyric.py
"""

import lyrics


def test_case_is_string():
    assert type(lyrics.test_case()) == str


def test_build_address():
    artist = 'eminem'
    song = 'lose-yourself'
    address = lyrics.build_address(artist, song)
    assert (artist in address and song in address)


def test_extract_lyrics():
    url = 'http://www.songlyrics.com/eminem/lose-yourself-lyrics/'
    assert type(lyrics.extract_lyrics(url)) == str

