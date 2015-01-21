# -*- coding: utf-8 -*-
import urllib
import json

def _parse_single_definition(unparsedDefinition):
    parsed = {'definition' : unparsedDefinition['difino']}
    parsed['examples'] = [{'example' : example['ekzemplo']}
                          for example in unparsedDefinition['ekzemploj']]
    return parsed


def _parse_definitions(unparsedDefinitions):
    return [_parse_single_definition(singleDefinition) for singleDefinition in unparsedDefinitions]


def find_definition(word, find_function):
    unparsedDefinition = find_function(word)
    return {'definitions' : _parse_definitions(unparsedDefinition['difinoj']),
            'word' : unparsedDefinition['vorto']}
