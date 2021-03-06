# -*- coding: utf-8 -*-
import urllib
import json
import string


def _get_json(url):
    print url
    return json.loads(urllib.urlopen(url).read())


def _escape_utf_characters(word):
    return urllib.quote(word.lower().encode('utf-8'))


def _lookup(word):
    return _get_json(
        "http://www.simplavortaro.org/api/v1/trovi/%s" %
        _escape_utf_characters(word))


def _find_definition(word):
    return _get_json(
        "http://www.simplavortaro.org/api/v1/vorto/%s" %
        _escape_utf_characters(word))


def _parse_subdefinitions(subdefinitions):
    """Parses subdefinitions of a word"""
    parsed = {'definition': subdefinitions['difino']}
    parsed['examples'] = [
        {
            'example': example['ekzemplo']
        } for example in subdefinitions['ekzemploj']]
    return parsed


def _parse_single_definition(unparsedDefinition):
    """Parses a single definition from Eo json to the internal format"""
    parsed = {'definition': unparsedDefinition['difino']}
    parsed['subdefinitions'] = [
        _parse_subdefinitions(subdefinition)
        for subdefinition in unparsedDefinition['pludifinoj']
    ]
        
    parsed['examples'] = [
        {'example': example['ekzemplo']}
        for example in unparsedDefinition['ekzemploj']
    ]
    return parsed


def _parse_definitions(unparsedDefinitions):
    return [
        _parse_single_definition(singleDefinition)
        for singleDefinition in unparsedDefinitions
    ]


def _find_full_definition(word, find_function):
    unparsedDefinition = find_function(word)
    return {
        'definitions': _parse_definitions(unparsedDefinition['difinoj']),
        'word': unparsedDefinition['vorto']
    }


def _lookup_word(word, find_function):
    searchResult = find_function(word)
    precise = searchResult['preciza']
    if len(precise) == 0:
        return None
    else:
        # Let's assume, that the first one is the right one
        return precise[0]


def _remove_grammatical_endings(word):
    # Removes plural and accustive ending from the word

    # Check nouns
    if word.endswith('oj') or word.endswith('on'):
        return word[:-1]
    if word.endswith('ojn'):
        return word[:-2]

    # Check adjectives
    if word.endswith('aj') or word.endswith('an'):
        return word[:-1]
    if word.endswith('ajn'):
        return word[:-2]
    
    # Check verbs
    if any([
            word.endswith('as'), word.endswith('is'),
            word.endswith('os'),  word.endswith('us'),
    ]):
        return word[:-2] + 'i'
    if word.endswith('u'):
        return word[:-1]
    return word


def find_definition(word):
    lookupResult = _lookup_word(word, _lookup)
    if lookupResult is not None:
        return _find_full_definition(lookupResult, _find_definition)
    else:
        return None


def split_proverb_into_words(proverb):
    exclude = set(string.punctuation)
    return ''.join(ch for ch in proverb if ch not in exclude).lower().split()


class TestEndingStriping(object):
    def test_ground_forms_not_changed(self):
        assert 'patro' == _remove_grammatical_endings('patro')
        assert 'grava' == _remove_grammatical_endings('grava')

    def test_plural_removal(self):
        assert 'patro' == _remove_grammatical_endings('patroj')
        assert 'grava' == _remove_grammatical_endings('gravaj')
    
    def test_accusative_removal(self):
        assert 'patro' == _remove_grammatical_endings('patron')
        assert 'grava' == _remove_grammatical_endings('gravan')
    
    def test_plural_and_accusative_removal(self):
        assert 'patro' == _remove_grammatical_endings('patrojn')
        assert 'grava' == _remove_grammatical_endings('gravajn')

    def test_plej_remains_unchanged(self):
        assert 'plej' == _remove_grammatical_endings('plej')

    def test_verbs_converted_to_inifinitive(self):
        assert 'lerni' == _remove_grammatical_endings('lerni')
        assert 'lerni' == _remove_grammatical_endings('lernas')
        assert 'lerni' == _remove_grammatical_endings('lernis')
        assert 'lerni' == _remove_grammatical_endings('lernos')
        assert 'lerni' == _remove_grammatical_endings('lernus')
        assert 'lerni' == _remove_grammatical_endings('lernis')


class TestSentenceSplitting(object):
    def test_split(self):
        expected = ['mizero', 'plej', 'ekstreme', 'dio', 'plej', 'proksime']
        to_split = 'Mizero plej ekstreme, Dio plej proksime.'
        actual = split_proverb_into_words(to_split)
        assert expected == actual
