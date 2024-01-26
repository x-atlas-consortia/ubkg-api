# Utilities for handling parameters

from flask import request

def parameter_as_list(param_name: str) -> list[str]:
    """
    Normalizes varying forms of query strings into a list of strings.
    :param param_name: name of the parameter to format.

    An endpoint that accepts a multi-value parameter (such as sab) should be able to process values either as key/value
    pairs or as a single, URL-escaped list--i.e., for param_names in {A, B, C}
    ?param_name=A&param_name=B&param_name=C
    or
    ?param_name=A%2CB%2CC
    (%2C = comma)

    :return: a list of strings--e.g., ['A','B','C']
    """
    listparam=request.args.getlist(param_name)
    if len(listparam) == 1:
        # This may be from a URL-escaped list. The result of getlist would be a list with a single value--e.g.,
        #'A,B,C'. Split this into separate values.
        listparam = listparam[0].split(',')
    return listparam