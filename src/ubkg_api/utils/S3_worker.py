import logging
import time
import boto3
from botocore.exceptions import ClientError

# February 2025 - cloned from hubmap_commons repository.

#S3Worker is a helper class used primarily for stashing the results of large web service responses in an S3 object
#which can then be downloaded via http(s) from a client.

# Note: This command is not in the original file.
logger = logging.getLogger()

class S3Worker:

    #create an instance of the S3Worker, required initialization parameters are:
    # ACCESS_KEY_ID- the id of an AWS access id/key pair with access to write to a public S3 bucket
    # SECRET_ACCESS_KEY- the secret/key side of the AWS access id/key pair with access to write to a public S3 bucket
    # S3_BUCKET_NAME- the name of the AWS S3 bucket where the results/obect will be stashed
    # S3_OBJECT_URL_EXPIRATION_IN_SECS- the number of seconds that the object will be downloadable for
    # LARGE_RESPONSE_THRESHOLD - number of bytes of a maximum service Response, above which the
    #                            response will be stored as an Object in the S3 Bucket, and
    #                            a URL will be returned.
    # SERVICE_S3_OBJ_PREFIX - A prefix used to name objects for this service within the
    #                         AWS S3 Bucket shared by the services. The name
    #                         of Objects in the Bucket is not relevant to the service user.
    def __init__(self, ACCESS_KEY_ID, SECRET_ACCESS_KEY
                 , S3_BUCKET_NAME, S3_OBJECT_URL_EXPIRATION_IN_SECS
                 , LARGE_RESPONSE_THRESHOLD, SERVICE_S3_OBJ_PREFIX):

        try:
            self.aws_access_key_id = ACCESS_KEY_ID
            self.aws_secret_access_key = SECRET_ACCESS_KEY
            self.aws_s3_bucket_name = S3_BUCKET_NAME
            self.s3_object_url_expiration_in_secs = S3_OBJECT_URL_EXPIRATION_IN_SECS
            self.large_response_threshold = LARGE_RESPONSE_THRESHOLD
            self.service_s3_obj_prefix = SERVICE_S3_OBJ_PREFIX
            if self.large_response_threshold > 10*(2**20):
                raise Exception(f"Cannot initialize an S3Worker instance with a"
                                f" large response threshold of {LARGE_RESPONSE_THRESHOLD},"
                                f" since this above AWS Gateway API limit of {10*(2**20)}.")
        except KeyError as ke:
            raise Exception(f"Expected configuration failed to load {ke} from constructor parameters.")

        try:
            self.s3resource = boto3.Session(
                self.aws_access_key_id,
                self.aws_secret_access_key
            ).resource('s3')
            # try an operation just to verify the Resource works so that the except clause
            # is entered here rather than another method if configuration is not correct.
            self.s3resource.meta.client.head_bucket(Bucket=self.aws_s3_bucket_name)
        except ClientError as ce:
            raise Exception(f"Unable to access S3 Resource. ce={ce} with aws_access_key_id={self.aws_access_key_id}.")

    # Write an object to the configured bucket
    # INPUTS:
    #  theText- the text that will be written to the object
    #  aUUID- A unique id to idenify the object
    # RETURNS:
    #  object_key- A unique key to identify the object (used in create_URL_for_object
    def stash_text_as_object(self, theText, aUUID):
        large_response_bucket = self.s3resource.Bucket(self.aws_s3_bucket_name)
        object_key = f"{aUUID}_{len(theText)}_{str(time.time())}"
        obj = large_response_bucket.Object(object_key)
        try:
            obj.put(Body=theText)
            return object_key
        except ClientError as ce:
            raise Exception(f"Unable to access S3 Resource. {ce}.")

    # create a URL which can be used to download an object via http(s)
    # INPUTS:
    #   object_key- the object_key received from stash_text_as_object when an object was created
    # RETURNS:
    #   object_url- the created object URL as a response object from the boto S3Resource
    #               method generate_presigned_url
    def create_URL_for_object(self, object_key):
        try:
            response = self.s3resource.meta.client.generate_presigned_url('get_object',
                                                                          Params={'Bucket': self.aws_s3_bucket_name,
                                                                                  'Key': object_key},
                                                                          ExpiresIn=self.s3_object_url_expiration_in_secs)
            return response
        except ClientError as ce:
            raise Exception(f"Unable generate URL to {self.aws_s3_bucket_name}. ce={ce}.")

    # If the size of the response_body above the limit the service which instantiated this
    # S3Worker is configured to return, stash response_body text in the S3 Bucket which this
    # S3Worker was initialized to use. Return a URL for the S3 Object, which is valid until
    # it expires.
    def stash_response_body_if_big(self, response_body:str):
        # Since the calling service passed in a dictionary of settings for AWS S3, stash
        # any large responses there.  Otherwise, allow the response to be returned directly
        # as this function exits.
        if len(response_body) >= self.large_response_threshold:
            try:
                obj_key = self.stash_text_as_object(response_body, self.service_s3_obj_prefix)
                aws_presigned_url = self.create_URL_for_object(obj_key)
                return aws_presigned_url
            except Exception as s3exception:
                logger.error(   f"Error getting anS3Worker to handle len(response_body)="
                                f"{len(response_body)}.")
                logger.error(s3exception, exc_info=True)
                raise(f"Unexpected error storing large results in S3. See logs.")
        else:
            return None