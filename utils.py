import boto3
from botocore.exceptions import ClientError
from upload import s3, BUCKET_NAME

def get_objects(BUCKET_NAME):
    objects = []
    try:
        paginator = s3.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket = BUCKET_NAME):
            for obj in page.get('Contents', []):
                objects.append(obj['Key'])
    except ClientError as e:
        print(e)
        return False
    
    return objects