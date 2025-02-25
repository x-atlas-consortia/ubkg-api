# Wrapper for S3Worker object used for S3 redirection of large responses

import flask
from flask import jsonify, make_response, current_app
from .http_error_string import check_payload_size
from .S3_worker import S3Worker


def getstashurl(resp:str, s3w:S3Worker)-> flask.Response:
    """
    Stashes content to the S3 bucket configured in the S3Worker object of the Flask app.
    :param resp: a string assumed to be the response from an API endpoint.
    :param s3w: S3Worker object
    """

    try:
        s3_url = s3w.stash_response_body_if_big(str(resp))

        if s3_url is not None:
            return make_response(s3_url, 303)
    except:
        err = 'Unexpected error storing large results in S3'
        return make_response(err, 500)

def redirect_if_large(resp:str) -> flask.Response:
    """
    Checks the size of a string, assumed to be the response from an API endpoint.

    If the string does not exceed the size limit specified in configuration,
    the function returns the string as JSON.

    If the string exceeds the size limit configured in the app.cfg, the function returns
    one of the following:
    1. If S3 redirection is specified in the app.cfg,
       a. directs the S3Worker to stash the string in a file in a specified S3 bucket
       b. returns a URL that points to the stored string
    2. If S3 redirection is not specified, returns a custom HTTP 403 response.

    :param resp: a string assumed to be the response from an API endpoint.

    """

    respstr = str(resp)

    threshold = 0
    if 'LARGE_RESPONSE_THRESHOLD' in current_app.config:
        threshold = current_app.config['LARGE_RESPONSE_THRESHOLD']
    if threshold == '':
        threshold = 0

    if threshold > 0:

        if 'AWS_S3_BUCKET_NAME' in current_app.config:

            if len(respstr) > threshold:
                s3w = S3Worker(ACCESS_KEY_ID=current_app.config['AWS_ACCESS_KEY_ID']
                               , SECRET_ACCESS_KEY=current_app.config['AWS_SECRET_ACCESS_KEY']
                               , S3_BUCKET_NAME=current_app.config['AWS_S3_BUCKET_NAME']
                               , S3_OBJECT_URL_EXPIRATION_IN_SECS=current_app.config['AWS_OBJECT_URL_EXPIRATION_IN_SECS']
                               , LARGE_RESPONSE_THRESHOLD=current_app.config['LARGE_RESPONSE_THRESHOLD']
                               , SERVICE_S3_OBJ_PREFIX=current_app.config['AWS_S3_OBJECT_PREFIX'])
                return getstashurl(resp=jsonify(respstr),s3w=s3w)

        else:

            # S3 redirection has not been enabled. Use default payload size checking.
            # Return a 403 (not authorized) error if the response size exceeds the threshold.
            err = check_payload_size(payload=respstr, max_payload_size=threshold)
            if err != "ok":
                return make_response(err, 403)

    # Normal return
    return jsonify(resp)
