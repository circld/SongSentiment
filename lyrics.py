"""
Lyric scraper (http://www.songlyrics.com/)
- capture list of songs with invalid urls (don't fail, cont running)
"""

from bs4 import BeautifulSoup
import urllib2 as ul2
from re import subn
from string import lstrip, rstrip, lower


def test_case():
    return extract_lyrics(
        'http://www.songlyrics.com/air-supply/all-out-of-love-lyrics/')


def build_address(artist, title):
    base = 'http://www.songlyrics.com/%s/%s-lyrics/'
    artist = subn(r'\s+', '-', rstrip(lstrip(lower(artist))))[0]
    title = subn(r'\s+', '-', rstrip(lstrip(lower(title))))[0]
    return base % (artist, title)


def extract_lyrics(address):
    try:
        con = ul2.urlopen(address)
        html = con.readlines()
    except:
        print 'There was a problem opening URL.'
    finally:
        con.close()

    if html is not None:
        soup = BeautifulSoup(' '.join(html))
        lyrics = soup.select('p[id="songLyricsDiv"]')  # html
        lyrics = ', '.join([i.extract() for i in lyrics[0]])  # unicode (\n)
        lyrics = subn(r'(\n|[\W])', ' ', lyrics)[0]  # remove non-alphanumeric
        lyrics = subn(r'\s+', ' ', lyrics)[0]  # replace mult spaces with single
        return str(lyrics)

