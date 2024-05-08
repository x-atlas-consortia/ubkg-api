# coding: utf-8
# Common functions used for format HTTP error messages (404, 400) for endpoints.

from flask import request


def format_request_path(custom_err=None):
    """
    Formats the request path for an error string.
    :param custom_err: a custom error string
    :return:
    """
    # The request path will be one of three types:
    # 1. The final element will correspond to the endpoint (e.g., /field-descriptions)
    # 2. The penultimate element will correspond to the endpoint, and the final element will be a filter.
    # 3. A more complicated path, for which a custom error string can be provided.

    pathsplit = request.path.split('/')
    err = f"{pathsplit[0]} "
    if len(pathsplit) > 3:
        if custom_err is None:
            err = err + f" for query path '{request.path}'"
        else:
            err = f" for {custom_err}"
    elif len(pathsplit) == 3:
        err = err + f" for '{pathsplit[2]}'"
    else:
        err = err + f" for '{pathsplit[1]}'"

    return err  # + '. '


def format_request_query_string():
    """
    Formats the request query string for error messages.

    :return:
    """
    err = ''

    listerr = []
    for req in request.args:
        listerr.append(f"'{req}'='{request.args[req]}' ")

    if len(listerr) > 0:
        err = ' and query parameter'
        if len(listerr) > 1:
            err = err + 's'
        err = err + ' ' + ' ; '.join(listerr)

    return err


def format_request_body():
    err = ''

    # Calling request.get_json(silent=True) returns nothing for the case in which there is not a request body.
    reqjson = request.get_json(silent=True)
    if not (reqjson is None or reqjson == []):
        err = f' Request body: {reqjson}'

    return err


def get_404_error_string(prompt_string=None, custom_request_path=None, timeout=None):
    """
    Formats an error string for a 404 response, accounting for optional parameters.
    :param prompt_string: - optional description of error
    :param timeout: optional timeout for timeboxed endpoints, in seconds
    :param custom_request_path: optional string to describe a value embedded in a complex request path
    --e.g., for /concept/C99999/paths/expand, custom_request_path might be "CUI='C99999'"
    :return: string
    """
    if prompt_string is None:
        err = "No values for "
    else:
        err = prompt_string

    err = err + format_request_path(custom_err=custom_request_path) + format_request_query_string() + format_request_body()

    if timeout is not None:
        errtimeout = f"{timeout} second"
        if timeout > 1:
            errtimeout = errtimeout + "s"

        err = err + f". Note that this endpoint is limited to an execution time of {errtimeout} " \
                    f" to prevent timeout errors."

    return err


def get_number_agreement(list_items=None):
    """
    Builds a clause with correct number agreement
    :param list_items: list of items
    :return:
    """
    if len(list_items) < 2:
        return ' is'
    else:
        return 's are'


def list_as_single_quoted_string(delim: str = ';', list_elements=None):
    """Converts the list of elements in list_elements into a string formatted with single quotes--
    e.g., ['a','b','c'] -> "'a'; 'b'; 'c'"

    """
    return f'{delim} '.join(f"'{x}'" for x in list_elements)


def validate_query_parameter_names(parameter_name_list=None) -> str:
    """
    Validates query parameter name in the querystring. Prepares the content of a 400 message if the
    querystring includes an unexpected parameter.
    :param parameter_name_list: list of parameter names
    :return:
    - "ok"
    - error string for a 400 error
    """

    if parameter_name_list is None:
        return f"Invalid query parameter. This endpoint does not take query parameters. " \
               f"Refer to the SmartAPI documentation for this endpoint for more information."

    for req in request.args:
        if req not in parameter_name_list:
            namelist = list_as_single_quoted_string(list_elements=parameter_name_list)
            prompt = get_number_agreement(list_items=parameter_name_list)
            return f"Invalid query parameter: '{req}'. The possible parameter name{prompt}: {namelist}. " \
                   f"Refer to the SmartAPI documentation for this endpoint for more information."

    return "ok"


def validate_required_parameters(required_parameter_list=None) -> str:
    """
    Validates that all required parameters have been specified in the query string. Prepares the content of a
    400 message unless all required parameters are present.

    :param required_parameter_list: list of names of required parameters.

    :return:
    - "ok"
    - error string for a 400 error

    """

    for param in required_parameter_list:
        if param not in request.args:
            namelist = list_as_single_quoted_string(list_elements=required_parameter_list)
            prompt = get_number_agreement(list_items=required_parameter_list)
            return f"Missing query parameter: '{param}'. The required parameter{prompt}: {namelist}. " \
                   f"Refer to the SmartAPI documentation for this endpoint for more information."

    return "ok"


def validate_parameter_value_in_enum(param_name=None, param_value=None, enum_list=None):
    """
    Verifies that a parameter's value is a member of a defined set--i.e., the equivalent of in an enumeration.
    :param enum_list: list of enum values
    :param param_value: value to validate
    :param param_name: parameter name
    :return:
    --"ok"
    --error string suitable for a 400 message
    """

    if param_value is None:
        return "ok"

    if param_name is None:
        return "ok"

    if param_value not in enum_list:
        namelist = list_as_single_quoted_string(list_elements=enum_list)
        prompt = get_number_agreement(enum_list)
        return f"Invalid value for parameter: '{param_name}'. The possible parameter value{prompt}: {namelist}. " \
               f"Refer to the SmartAPI documentation for this endpoint for more information."

    return "ok"


def validate_parameter_is_numeric(param_name=None, param_value: str = '') -> str:
    """
    Verifies that a request parameter's value is numeric
    :param param_name: name of the parameter
    :param param_value: value of the parameter
    :return:
    --"ok"
    --error string suitable for a 400 message
    """

    if not param_value.lstrip('-').isnumeric():
        return f"Invalid value ({param_value}) for parameter '{param_name}'.  The parameter must be numeric."

    return "ok"


def validate_parameter_is_nonnegative(param_name=None, param_value: str = '') -> str:
    """
    Verifies that a request parameter's value is not negative
    :param param_name: name of the parameter
    :param param_value: value of the parameter
    :return:
    --"ok"
    --error string suitable for a 400 message
    """

    if param_value is None:
        return "ok"
    err = validate_parameter_is_numeric(param_name=param_name, param_value=param_value)
    if err != 'ok':
        return err

    if int(param_value) < 0:
        return f"Invalid value ({param_value}) for parameter '{param_name}'. The parameter cannot be negative."

    return "ok"


def validate_parameter_range_order(min_name: str, min_value: str, max_name: str, max_value: str) -> str:
    """
       Verifies that a range of parameter values is properly ordered.
        :param min_name: name of mininum parameter
        :param min_value: value for minimum parameter
        :param max_name: name of maximum parameter
        :param max_value: value for maximum parameter
       :return:
       --"ok"
       --error string suitable for a 400 message
       """

    if int(min_value) > int(max_value):
        return f"Invalid parameter values: '{min_name}' ({min_value}) greater than '{max_name}' ({max_value}). "

    return "ok"


def check_payload_size(payload: str, max_payload_size: int) -> str:
    """
    Verifies that a payload string is within payload limits.
    :param payload: string from a query response
    :param max_payload_size: maximum payload size
    """

    payload_size = len(str(payload))
    if payload_size > max_payload_size:
        return f"The size of the response to the endpoint with the specified parameters " \
               f"({int(payload_size)/1024} MB) exceeds the payload limit" \
               f" of {int(max_payload_size)/1024} MB."

    return "ok"


def check_neo4j_version_compatibility(query_version: str, instance_version: str) -> str:
    """
    Checks whether a query can be executed against the instance of UBKG.

    :param query_version: version of minimal version of neo4j Cypher that the query requires
    :param instance_version: the version of the current UBKG instance

    Assumes that version strings are in format major.minor.subminor--e.g., 5.11.0

    """

    int_instance_version = int(instance_version.replace('.', ''))
    int_query_version = int(query_version.replace('.', ''))

    if int_instance_version < int_query_version:
        return f"This functionality requires at least version {query_version} of neo4j."

    return "ok"

def check_max_mindepth(mindepth: int, max_mindepth: int) -> str:
    """
    Validates that the value of mindepth does not exceed a maximum value.
    This is a workaround for the issue in which APOC timeboxing does not work for path-related
    endpoints that return a paths object.

    """
    if mindepth > max_mindepth:
        return f"The maximum value of 'mindepth' for this endpoint is {max_mindepth}. " \
               f"Larger values of 'mindepth' result in queries that will exceed the server timeout."
    return "ok"
