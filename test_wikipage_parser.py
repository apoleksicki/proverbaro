import pytest
import unittest
from wikipage_parser import ProverbsWikipageParser




def test_simple_li():
    parser = ProverbsWikipageParser()
    parser.feed('<li>Aliloka ĉielo estas sama ĉielo.</li>')
    assert 1 == len(parser.parsed)
    assert 'Aliloka ĉielo estas sama ĉielo.' == parser.parsed[0]




if __name__ == '__main__':
    pytest.main(['-x', './'])
