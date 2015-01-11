# -*- coding: utf-8 -*-
import json
from translation_util import find_definition

def _read_json(filename):
    with open('test_resources\%s' % filename, 'r') as f:
        return json.loads(f.read())


def _read_saluti_json(word):
    return _read_json('saluti.json')

def test_find_definition_of_saluti():
    expected = _read_json('converted_saluti.json')
    salutidef = find_definition('saluti', _read_saluti_json)
    print expected
    print salutidef
    assert expected == salutidef
