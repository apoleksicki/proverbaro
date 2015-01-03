# -*- coding: utf-8 -*-
import pytest
import unittest
from wikipage_parser import ProverbsWikipageParser


def _simple_test(expected, to_parse):
    parser = ProverbsWikipageParser()
    parser.feed(to_parse)
    assert 1 == len(parser.parsed)
    assert expected == parser.parsed[0]


def test_simple_li():
    _simple_test('Aliloka ĉielo estas sama ĉielo.',
                 '<li>Aliloka ĉielo estas sama ĉielo.</li>')


def test_li_with_href():
    to_parse = '<li>Almozpetanto <a href="/wiki/Sin%C4%9Deno"'\
    'title="Sinĝeno">sinĝena</a> restas kun sako malplena.</li>'
    _simple_test('Almozpetanto sinĝena restas kun sako malplena.', to_parse)


def test_li_with_multiple_href():
    to_parse = '<li>Vivi en <a href="/wiki/Silko" title="Silko">silko</a> '\
    'kaj <a href="/wiki/Veluro" title="Veluro">veluro</a>, en '\
    '<a href="/wiki/%C4%9Cojo" title="Ĝojo">ĝojo</a> kaj '\
    '<a href="/wiki/Plezuro" title="Plezuro">plezuro</a>.</li>'
    _simple_test('Vivi en silko kaj veluro, en ĝojo kaj plezuro.', to_parse)


if __name__ == '__main__':
    pytest.main(['-x', './'])
