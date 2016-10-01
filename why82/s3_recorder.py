import boto3
from botocore.exceptions import ClientError
import simplejson as json
from why82.settings import BUCKET_NAME


class S3Recorder:
    @staticmethod
    def record(key, json_string, overwrite=False):
        print('Saving %s' % key)
        if (not overwrite) and S3Recorder.does_key_exist(key):
            print('%s already exists. Not overwriting.' % key)
        else:
            s3_client = boto3.resource('s3')
            s3_client.Bucket(BUCKET_NAME).put_object(
                    ContentType='application/json', Key=key,
                    Body=json_string
            )
            print('%s saved to S3' % key)

    @staticmethod
    def does_key_exist(key):
        s3_client = boto3.client('s3')
        try:
            s3_client.head_object(Bucket=BUCKET_NAME, Key=key)
        except ClientError:
            return False
        else:
            return True

    @staticmethod
    def load_json_file(key, bucket=BUCKET_NAME):
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=bucket, Key=key)
        return json.loads(response['Body'].read())
