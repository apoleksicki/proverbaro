# -*- coding: utf-8 -*-
import urllib
from HTMLParser import HTMLParser

def fetch_wikpage():
    page = urllib.urlopen("http://eo.wikiquote.org/wiki/Zamenhofa_proverbaro")

    file = open('website.html', 'w')
    file.write(page.read())
    file.close()

def parse_wikipage():
    parser = ProverbsWikipageParser()
    with open('website.html', 'r') as input_file:
        with open('output.txt', 'w') as output_file:
            output_file.write(parser.feed(input_file.read()))

class ProverbsWikipageParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._parsed = []
        self._parsing_proverb = False
        self._proverb = None

    def _change_state(self, tag):
        if tag == 'li':
            self._parsing_proverb = not self._parsing_proverb
            self._proverb = ''
    def handle_starttag(self, tag, attrs):
        self._change_state(tag)
    def handle_endtag(self, tag):
        if self._parsing_proverb and tag == 'li':
            self._parsed.append(self._proverb)
            print(self._proverb)
        self._change_state(tag)
    def handle_data(self, data):
        if self._parsing_proverb:
            self._proverb += data
    @property
    def parsed(self):
        return self._parsed

def parse(to_parse):
    parser = ProverbsWikipageParser()
    parser.feed(to_parse)
    print len(parser.parsed)
    parser._parsed

to_parse = '<li>Almozpetanto <a href="/wiki/Sin%C4%9Deno" title="Sinĝeno">sinĝena</a> restas kun sako malplena.</li>'

if __name__ == '__main__':
    fetch_wikpage()
    parse_wikipage()
