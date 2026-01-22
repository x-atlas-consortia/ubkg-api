"""
January 2026
Open API base model class.
This has been re-introduced to the ubkg-api to resolve dependency issues in the hs-ontology-api.

The hs-ontology-api currently uses subclasses of the OpenAPI model class to translate Cypher
streams from the neo4j driver. This was the original behavior of the ubkg-api.

Once the hs-ontology-api endpoints have been refactored to where they directly use JSON streams
instead of translating Cypher streams, classes related to OpenAPI will be removed from ubkg-api.
"""
import pprint

import six
import typing

from . import util

T = typing.TypeVar('T')


class Model(object):
    # openapiTypes: The key is attribute name and the
    # value is attribute type.
    openapi_types: typing.Dict[str, type] = {}

    # attributeMap: The key is attribute name and the
    # value is json key in definition.
    attribute_map: typing.Dict[str, str] = {}

    @classmethod
    def from_dict(cls: typing.Type[T], dikt) -> T:
        """Returns the dict as a model"""
        return util.deserialize_model(dikt, cls)

    def to_dict(self):
        """Returns the model properties as a dict

        :rtype: dict
        """
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model

        :rtype: str
        """
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other