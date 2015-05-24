# -*- coding: utf-8 -*-
import json

from translation_util import _find_definition, _find_full_definition

def _read_json(filename):
    with open('test_resources\%s' % filename, 'r') as f:
        return json.loads(f.read())


def _read_saluti_json(filename):
    def read_definition(word):
        return _read_json(filename)
    return read_definition


def test_convert_saluti_definition_1():
    expected = _read_json('converted_saluti_def_1.json')
    saluti1def = _parse_single_definition(_read_json('saluti_def_1.json'))
    assert expected == saluti1def


def test_find_definition_of_saluti():
    expected = _read_json('converted_saluti.json')
    salutidef = _find_full_definition('saluti', _read_saluti_json('saluti.json'))
    assert expected == salutidef
