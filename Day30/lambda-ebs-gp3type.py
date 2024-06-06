import json
import boto3
import time

def lambda_handler(event, context):
    client = boto3.client("ec2", region_name="your-region")
    resp = client.describe_volumes().get("Volumes", [])
    unattached_gp3_vols = []
    time.sleep(30)
    
    for vol in resp:
        if len(vol["Attachments"]) == 0 and vol["VolumeType"] == "gp3":
            volid = vol["VolumeId"]
            print(f"gp3 Volume {volid} is not attached and will be deleted")
            unattached_gp3_vols.append(vol["VolumeId"])
        else:
            volid = vol["VolumeId"]
            # Uncomment the line below to print details of attached volumes or non-gp3 volumes if needed
            # print(f"Volume {volid} is attached or not a gp3 type")

    print(f"The gp3 Volumes which are available are {unattached_gp3_vols}")
    ec2_resource = boto3.resource("ec2", region_name="your-region")
    
    for vol in unattached_gp3_vols:
        volume = ec2_resource.Volume(vol)
        volume.delete()
