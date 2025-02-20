# Interface to S3Worker object for redirection of large responses

import flask
from flask import jsonify, make_response, current_app
from .http_error_string import check_payload_size

def getstashurl(resp:str)-> flask.Response:
    """
    Stashes content to the S3 bucket configured in the S3Worker object of the Flask app.
    :param resp: a string assumed to be the response from an API endpoint.
    """

    try:
        s3_url = current_app.s3worker.stash_response_body_if_big(str(resp))

        if s3_url is not None:
            return make_response(s3_url, 303)
    except:
        err = 'Unexpected error storing large results in S3'
        return make_response(err, 500)

def redirect_if_large(resp:str) -> flask.Response:
    """
    Checks the size of a string, assumed to be the response from an API endpoint.

    If the string exceeds the size limit configured in the S3Worker, the function:
    1. directs the S3Worker to stash the string in a file in a specified S3 bucket
    2. returns the URL pointing to the stored string

    If the string does not exceed the size limit, the function returns the string as JSON.

    :param resp: a string assumed to be the response from an API endpoint.

    """

    respstr = str(resp)
    # Check whether S3 redirection has been enabled, as evidenced by the existence
    # of a S3Worker object on the Flask app.
    try:
        # A threshold of 0 indicates that S3 redirection is disabled.
        print('DEBUG ', current_app.s3worker)
        if current_app.s3worker.large_response_threshold > 0:
            if len(respstr) > current_app.s3worker.large_response_threshold:
                return getstashurl(resp=respstr)

    except AttributeError:
        # S3 redirection has not been enabled. Use default payload size checking.
        # Return a 413 (payload too large) error if the response size exceeds the configured payload limit, which should be
        # smaller than the API gateway payload limit. The payload limit is a property of the Flask app's
        # neo4jConnectionHelper object.
        err = check_payload_size(payload=respstr, max_payload_size=current_app.neo4jConnectionHelper.instance().payloadlimit)
        if err != "ok":
            return make_response(err, 413)

    # Normal return
    return jsonify(resp)





