import boto3
from botocore.exceptions import ClientError

from why82.constants import BUCKET_NAME


class S3Recorder:
    @staticmethod
    def record(date, name, json_string, overwrite=False):
        key = '%s/%s-%s.json' % (date.year, date.strftime('%Y-%m-%d'), name)
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
