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

def getconfigval(configkey:str) -> str:
    """
    Obtains the value for a key from the application configuration, based on
    context.

    If the ubkg-api is running standalone (development), configuration keys are
    obtained from the ubkg-api's app.cfg.

    If the ubkg-api is instantiated in a child api, configuration keys from the child api's
    app.cfg are set as attributes of the ubkg-api instance. In particular, in case of
    conflict, the child api's configuration takes precedence.

    :param configkey: the key to search
    """

    print(current_app)
    configval = ''
    if hasattr(current_app, configkey):
        print('CHILD API')
        # loaded in child api
        configval = current_app.configkey
    else:
        # local
        print('LOCAL')
        if configkey in current_app.config:
            configval = current_app.config[configkey]

    print('getconfigval', configkey, configval)
    return configval

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
    2. If S3 redirection is not specified, returns a custom HTTP 413 response.

    :param resp: a string assumed to be the response from an API endpoint.

    """

    respstr = str(resp)

    threshold = getconfigval('LARGE_RESPONSE_THRESHOLD')
    if threshold == '':
        threshold = 0

    if threshold > 0:

        if getconfigval('AWS_S3_BUCKET_NAME') != '':

            s3w = S3Worker(ACCESS_KEY_ID=getconfigval('AWS_ACCESS_KEY_ID')
                   , SECRET_ACCESS_KEY=getconfigval('AWS_SECRET_ACCESS_KEY')
                   , S3_BUCKET_NAME=getconfigval('AWS_S3_BUCKET_NAME')
                   , S3_OBJECT_URL_EXPIRATION_IN_SECS=getconfigval('AWS_OBJECT_URL_EXPIRATION_IN_SECS')
                   , LARGE_RESPONSE_THRESHOLD=getconfigval('LARGE_RESPONSE_THRESHOLD')
                   , SERVICE_S3_OBJ_PREFIX=getconfigval('AWS_S3_OBJECT_PREFIX'))

            if len(respstr) > threshold:
                    return getstashurl(resp=respstr,s3w=s3w)

        else:

            # S3 redirection has not been enabled. Use default payload size checking.
            # Return a 413 (payload too large) error if the response size exceeds the threshold.
            err = check_payload_size(payload=respstr, max_payload_size=threshold)
            if err != "ok":
                return make_response(err, 413)

    # Normal return
    return jsonify(resp)
