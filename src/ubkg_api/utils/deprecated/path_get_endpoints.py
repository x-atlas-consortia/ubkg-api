# Utility for controllers to extract path origins from ConceptPath responses returned from path-related queries.

import os
import sys
# The following allows for an absolute import from an adjacent script directory--i.e., up and over instead of down.
# Find the absolute path. (This assumes that this script is being called from build_csv.py.)
fpath = os.path.dirname(os.getcwd())
print(fpath)
fpath = os.path.join(fpath, 'utils')
sys.path.append(fpath)
# from models.base_model_ import Model
from models.concept_path import ConceptPath
from models.concept_prefterm import ConceptPrefterm


def get_origin(pathlist: list[ConceptPath]) -> ConceptPrefterm:

    """
    Each path in the ConceptPath object contains its origin--i.e., the target of the first hop.
    Extract the origin from the first hop of the first path and write to a common object outside the path list,
    as syntactic sugar. This does not use a model class, but assumes that the concepts_expand_get_logic used
    model classes when building its hop objects.

    """

    first_path = pathlist[0]
    first_path_hops = first_path.get('hops')

    first_path_first_hop = first_path_hops[0]
    origin = first_path_first_hop.get('target')

    return origin


def get_terminus(pathlist: list[ConceptPath]) -> ConceptPrefterm:
    """
    Each path in the ConceptPath object contains its terminus--i.e., the source of the last hop.
    Extract the terminus from the last hop of the (first) path and write to a common object outside the path list,
    as syntactic sugar. This does not use a model class, but assumes that the concepts_expand_get_logic used
    model classes when building its hop objects.

    The use case for this function is to return the terminus of the shortest path, and assumes one path.

    :param pathlist: A list of path hops

    """

    first_path = pathlist[0]
    first_path_hops = first_path.get('hops')
    first_path_last_hop = first_path_hops[len(first_path_hops)-1]
    source = first_path_last_hop.get('source')

    return source
