import boto3

def write_to_dynamo(item_obj: dict):
    dynamodb = boto3.resource(
        'dynamodb',
        region_name='us-west-1',
        aws_access_key_id='AKIAUEGXZZHFW6U6QN2L',
        aws_secret_access_key='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'
        )
    table = dynamodb.Table('cmpeats')
    response = table.put_item(
        Item=item_obj
    )
    print(response)


def read_from_dynamo(item_obj: dict):
    dynamodb = boto3.resource(
        'dynamodb',
        region_name='us-west-1',
        aws_access_key_id='AKIAUEGXZZHFW6U6QN2L',
        aws_secret_access_key='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'
    )
    table = dynamodb.Table('cmpeats')
    response = table.get_item(
        Key=item_obj
    )
    return response