import boto3
import json

DRYRUN = False

ec2vm = boto3.client('ec2')

def Create_EC2(AMI,client1):
    response = client1.run_instances(
        ImageId = AMI,
        InstanceType = 't2.micro',
        MaxCount = 1,
        MinCount = 1,
        DryRun = DRYRUN
        )
    ec2ID = response['Instances'][0]['InstanceId']
    return ec2ID

def Get_Image(client):
    amiresponse = client.describe_images(
        Filters=[
            {
                'Name':'name',
                'Values':[
                    'amzn2-ami-hvm*'
                ]
            }
        ]
    )
    return amiresponse

allimagelist = Get_Image(ec2vm)

imageID = allimagelist['Images'][0]['ImageId']

ec2_instance = boto3.resource('ec2')

ec2ID = Create_EC2(imageID,ec2vm)
print(ec2ID)



instance = ec2_instance.Instance(id=ec2ID)
instance.wait_until_running()

print(instance.public_ip_address)
print(instance.tags)
instance.create_tags(
    Tags=[
        {'Key':'Name',
        'Value':'Ben'
        }
    ]
)



print(instance.tags)

instance.terminate()

instance.wait_until_terminated()


