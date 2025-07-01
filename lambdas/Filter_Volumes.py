import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    response = ec2.describe_volumes(
        Filters=[{'Name': 'volume-type', 'Values': ['gp2']}]
    )
    
    filtered = []
    for vol in response['Volumes']:
        tags = {t['Key']: t['Value'] for t in vol.get('Tags', [])}
        if tags.get('AutoConvert', '').lower() == 'true':
            filtered.append({
                'VolumeId': vol['VolumeId'],
                'Size': vol['Size'],
                'Region': ec2.meta.region_name,
                'InstanceId': vol['Attachments'][0]['InstanceId'] if vol['Attachments'] else None
            })
    
    return filtered
