"""
Lyric scraper (http://www.songlyrics.com/)
- capture list of songs with invalid urls (don't fail, cont running)
- how to handle song not in songlyrics.com? alternate lyrics site?
"""

from bs4 import BeautifulSoup
import urllib2 as ul2
from re import subn
from string import lstrip, rstrip, lower, punctuation


def test_case():
    return extract_lyrics('air supply', 'all out of love')


def build_address(artist, title):
    base = 'http://www.songlyrics.com/%s/%s-lyrics/'
    artist = rstrip(lstrip(lower(artist)))
    title = rstrip(lstrip(lower(title)))
    # remove leading 'the ', ampersands, or
    # anything following a slash or variants of featuring
    artist = subn(r"(^the |/.*$|[&]| and his band| f.{5}ing.*$|" +
                  r" ft[.].*$| feat[.]? .*$)", '', artist)[0]
    # replace space(s) or punctuation with hyphen
    artist = subn(r"(\s+|[',.])", '-', artist)[0]
    # remove non-leading parens and everything after
    title = subn(r'(?<!^)[(].*?[)].*$', '', title)[0]
    # remove leading parens (leave content) & all consecutive
    # punctuation at EOL
    title = subn(r'(^[(]|[)]|[%s]+$|/.*$)' % punctuation,
                 '', rstrip(title))[0]
    # replace space or (multiple) punctuation followed by space with a hyphen
    title = subn(r"(\s|[',.)]+\s*)", '-', rstrip(title))[0]
    return base % (artist, title)


def extract_lyrics(artist, title):
    song_url = build_address(artist, title)
    try:
        con = ul2.urlopen(song_url)
        html = con.readlines()
    except:
        return song_url
    finally:
        if 'con' in locals().keys():
            con.close()

    if html is not None:
        soup = BeautifulSoup(' '.join(html))
        lyrics_tag = soup.select('p[id="songLyricsDiv"]')  # html
        # handle empty list (ie, no lyrics in html)
        if not lyrics_tag:
            return song_url
        # unicode (\n); hasattr() to ignore Tag elements
        lyrics = ', '.join([i.extract() for i in lyrics_tag[0]
                            if not hasattr(i, 'content')])
        lyrics = subn(r'(\n|[\W])', ' ', lyrics)[0]  # remove non-alphanumeric
        lyrics = subn(r'\s+', ' ', lyrics)[0]  # replace mult spaces with single
        if lyrics == '':
            return song_url
        return str(lyrics)

