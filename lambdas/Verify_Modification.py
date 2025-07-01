import boto3
import time

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2', region_name='ap-south-1')  # change to your region

    results = []

    for item in event:
        volume_id = item.get('VolumeId')

        try:
            # Wait a few seconds for modification to complete (optional)
            time.sleep(10)

            response = ec2_client.describe_volumes(VolumeIds=[volume_id])
            volume = response['Volumes'][0]

            volume_type = volume['VolumeType']
            state = volume['State']

            if volume_type == 'gp3':
                status = "completed"
            else:
                status = f"in-progress or failed (current type: {volume_type})"

            results.append({
                "VolumeId": volume_id,
                "VolumeType": volume_type,
                "State": state,
                "ModificationStatus": status
            })

        except Exception as e:
            results.append({
                "VolumeId": volume_id,
                "ModificationStatus": f"Error: {str(e)}"
            })

    return results
