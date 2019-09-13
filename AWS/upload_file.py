# Uploads a file to S3 bucket
# See AWS doc https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
# run using the following command: 
### python3 uploadfile.py file_name bucket_name object_name
# e.g.: python3 uploadfile.py enwiki-20190901-pages-articles-multistream-index5.txt-p352690p565312 wikibuckets test_eng_wiki20190901-pages-multistream-index5.txt

import sys
import time
import csv

import logging
import boto3
from botocore.exceptions import ClientError

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def main():
    start_time = time.time()
    sys_arv = sys.argv
    file_name = sys.argv[1]
    bucket = sys.argv[2]
    object_name = sys.argv[3]
    upload_file(file_name, bucket, object_name)
    print('File uploaded')

if __name__ == '__main__':
    main()


