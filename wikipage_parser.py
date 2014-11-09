import urllib
from HTMLParser import HTMLParser

def fetch_wikpage():
    foo = urllib.urlopen("http://eo.wikiquote.org/wiki/Zamenhofa_proverbaro")

    file = open('website.html', 'w')

    print foo.read()

    file.write(foo.read())
    file.close()

class ProverbsWikipageParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._parsed = []
        self._parsing_proverb = False

    def _change_state(self, tag):
        if tag == 'li':
            self._parsing_proverb = not self._parsing_proverb

    def handle_starttag(self, tag, attrs):
        print "Encountered a start tag:", tag
        self._change_state(tag)
    def handle_endtag(self, tag):
        print "Encountered an end tag :", tag
        self._change_state(tag)
    def handle_data(self, data):
        if self._parsing_proverb:
            self._parsed.append(data)
    @property
    def parsed(self):
        return self._parsed

parser = ProverbsWikipageParser()
print len(parser.parsed)


foo = []
foo.append(1)
foo


parser.feed('<html><head><title>Test</title></head>'
            '<body><li>Parse me!</li></body></html>')

parser._parsed

