# -*- coding: utf-8 -*-
import urllib
import json

def _parse_single_definition(unparsedDefinition):
    parsed = {u'definition' : unparsedDefinition[u'difino']}
    parsed[u'examples'] = [{u'example' : example[u'ekzemplo']}
                          for example in unparsedDefinition[u'ekzemploj']]
    return parsed


def _parse_definitions(unparsedDefinitions):
    return [_parse_single_definition(singleDefinition) for singleDefinition in unparsedDefinitions]


def find_definition(word, find_function):
    unparsedDefinition = find_function(word)
    return {u'definitions' : _parse_definitions(unparsedDefinition[u'difinoj']),
            u'word' : unparsedDefinition['vorto']}
