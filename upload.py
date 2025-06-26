import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError
import os
import boto3
import json


load_dotenv()


def get_secret(secret_name, region_name="us-east-1"):
    secret_client = boto3.client('secretsmanager', region_name)

    try:
        response = secret_client.get_secret_value(SecretId=secret_name)

    except ClientError as e:
        pass

    if "SecretString" in response:
        return json.loads(response["SecretString"])
    else:
        return response["SecretBinary"]
    

secrets = get_secret("simples3", "eu-north-1")

# AWS credentials and bucket name
AWS_ACCESS_KEY = secrets.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = secrets.get("AWS_SECRET_KEY")
AWS_REGION = secrets.get("AWS_REGION", "us-east-1")
BUCKET_NAME = secrets.get("BUCKET_NAME")

# Create S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
)
