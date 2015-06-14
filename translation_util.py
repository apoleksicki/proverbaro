# -*- coding: utf-8 -*-
import logging
import urllib
import json
import pytest

def _get_json(url):
    print url
    return json.loads(urllib.urlopen(url).read())

def _lookup(word):
    return _get_json("http://www.simplavortaro.org/api/v1/trovi/%s" % word.lower())


def _find_definition(word):
    return _get_json("http://www.simplavortaro.org/api/v1/vorto/%s" % word)


def _parse_single_definition(unparsedDefinition):
    parsed = {'definition' : unparsedDefinition['difino']}
    parsed['examples'] = [{'example' : example['ekzemplo']}
                          for example in unparsedDefinition['ekzemploj']]
    return parsed


def _parse_definitions(unparsedDefinitions):
    return [_parse_single_definition(singleDefinition) for singleDefinition in unparsedDefinitions]


def _find_full_definition(word, find_function):
    unparsedDefinition = find_function(word)
    return {'definitions' : _parse_definitions(unparsedDefinition['difinoj']),
            'word' : unparsedDefinition['vorto']}


def _lookup_word(word, find_function):
    searchResult = find_function(word)
    precise = searchResult['preciza']
    if len(precise) == 0:
        return None
    else:
        #Let's assume, that the first one is the right one
        return precise[0]


def _remove_grammatical_endings(word):
    #Removes plural and accustive ending from the word
    if word[-1] == 'j':
        return word[:-1]
    if word[-1] == 'n':
        if word[-2] == 'j':
            return word[:-2]
        else:
            return word[:-1]

def find_definition(word):
    lookupResult = _lookup_word(word, _lookup)
    if lookupResult is not None:
        return _find_full_definition(lookupResult, _find_definition)
    else:
        return None


class TestEndingStriping(object):
    def test_plural_removal(self):
        assert 'patro' == _remove_grammatical_endings('patroj')
    
    def test_accusative_removal(self):
        assert 'patro' == _remove_grammatical_endings('patron')
    
    def test_plural_and_accusative_removal(self):
        assert 'patro' == _remove_grammatical_endings('patrojn')        
