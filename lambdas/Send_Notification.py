import boto3
import os

sns = boto3.client('sns')
topic_arn = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    for vol in event:
        volume_id = vol.get("VolumeId")
        region = vol.get("Region")
        status = vol.get("Status", "unknown")

        sns.publish(
            TopicArn=topic_arn,
            Subject='EBS Volume Converted',
            Message=f"Volume {volume_id} in region {region} status: {status}"
        )

    return {"Message": "Notifications sent."}
