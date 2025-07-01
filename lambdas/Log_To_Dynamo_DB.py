import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EBS_Conversion_Logs')

def lambda_handler(event, context):
    for vol in event:
        table.put_item(Item={
            'VolumeID': vol['VolumeId'],
            'InstanceID': vol['InstanceId'],
            'Region': vol['Region'],
            'Size': vol['Size'],
            'Status': 'Pending',
            'Timestamp': datetime.utcnow().isoformat(),
            'OldType': 'gp2'
        })
    return event
