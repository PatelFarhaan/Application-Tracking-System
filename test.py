import datetime
import boto3
import json

dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-west-1',
    aws_access_key_id='AKIAUEGXZZHFW6U6QN2L',
    aws_secret_access_key='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'
    )
table = dynamodb.Table('ats')
response = table.put_item(
    Item={
        'resumes': json.dumps({
            1:
                json.dumps({
                    2: 3
                }))
        }
    }
)