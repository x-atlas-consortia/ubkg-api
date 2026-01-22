"""
January 2026
Open API base model class.
This has been re-introduced to the ubkg-api to resolve dependency issues in the hs-ontology-api.

The hs-ontology-api currently uses subclasses of the OpenAPI model class to translate Cypher
streams from the neo4j driver. This was the original behavior of the ubkg-api.

Once the hs-ontology-api endpoints have been refactored to where they directly use JSON streams
instead of translating Cypher streams, classes related to OpenAPI will be removed from ubkg-api.
"""
# coding: utf-8

import sys

if sys.version_info < (3, 7):
    import typing

    def is_generic(klass):
        """ Determine whether klass is a generic class """
        return type(klass) == typing.GenericMeta

    def is_dict(klass):
        """ Determine whether klass is a Dict """
        return klass.__extra__ == dict

    def is_list(klass):
        """ Determine whether klass is a List """
        return klass.__extra__ == list

else:

    def is_generic(klass):
        """ Determine whether klass is a generic class """
        return hasattr(klass, '__origin__')

    def is_dict(klass):
        """ Determine whether klass is a Dict """
        return klass.__origin__ == dict

    def is_list(klass):
        """ Determine whether klass is a List """
        return klass.__origin__ == list