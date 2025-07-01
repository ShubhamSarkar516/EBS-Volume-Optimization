import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    for vol in event:
        try:
            ec2.modify_volume(
                VolumeId=vol['VolumeId'],
                VolumeType='gp3'
            )
            vol['Status'] = 'ModificationStarted'
        except Exception as e:
            vol['Status'] = f"Error: {str(e)}"
    return event
