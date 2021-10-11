import boto3
import json
import argparse
import string
import random
import botocore
import ec2



s3 = boto3.client('s3')

bucket_name = 'week6-bucket-bdickerson1'

parser = argparse.ArgumentParser(description="This is to allow arguments")

parser.add_argument('-s','--site-name',dest='site_name', default='', type=str, help='enter a unique bucket name')
args = parser.parse_args()
#print(args.site_name)
if not args.site_name:
    print(f"no site name, using randomly generated name")
    bucket_name += "".join(random.choices(string.ascii_lowercase, k=10))
else:
    bucket_name = args.site_name

try:
    response = s3.create_bucket(Bucket=bucket_name)
    #print(response)

    bucket_policy = {
        'Version': '2012-10-17',
        'Statement': [{
            'Sid': 'AddPerm',
            'Effect': 'Allow',
            'Principal': '*',
            'Action': ['s3:GetObject'],
            'Resource': "arn:aws:s3:::%s/*" % bucket_name
        }] 
    } 
    bucket_policy = json.dumps(bucket_policy, indent=4)
    #print(bucket_policy)

    policy_response = s3.put_bucket_policy(Bucket=bucket_name,Policy=bucket_policy)
    #print (policy_response)

    website_response = s3.put_bucket_website(
        Bucket=bucket_name,
        WebsiteConfiguration={
        'ErrorDocument': {'Key': 'error1.html'},
        'IndexDocument': {'Suffix': 'index1.html'},
        }
    )
    #print(website_response)
    index_file = open('index.html', 'rb')
    s3.put_object(Body=index_file,Bucket=bucket_name,Key='index.html', ContentType='text/html')
    index_file.close()

    error_file = open('error.html', 'rb')
    s3.put_object(Body=error_file,Bucket=bucket_name,Key='error.html', ContentType='text/html')
    error_file.close()

except botocore.exceptions.ClientError as error:
    #This handles the Invalid Token in the aws creds file
    if error.response['Error']['Code'] == 'InvalidToken':
        print("Please updated your aws creds in a valid token")
    else:
        #This handles the us-east-2 error in the aws config file
        if error.response['Error']['Code'] == 'IllegalLocationConstraintException':
            print("Please change the region in aws config file")
        else:
            print(f"some other error occured {error}")

#  I wrote this part when I thought i need to handle 2 additional errors.
#  I call the ec2.py script and have some of the stuff commented out in order to 
#  produce the errors. 
#  The first error is no AMI id in the create_EC2 function
#  The second error is a reference to webSG security group that doesn't exist


#try:
#    ec2_client = boto3.client('ec2')
#    image_id = ec2.Get_Image(ec2_client)['Images'][0]['ImageId']
#    instance_id = ec2.Create_EC2(image_id,ec2_client)

#except botocore.exceptions.ClientError as error:
#    if error.response['Error']['Code'] == 'MissingParameter':
#        print("Please check for a missing required EC2 parameter like AMI")
#    else:

#        #This handles the issue where a security group is in the EC2.py script, but it doesn't actually exist

#        if error.response['Error']['Code'] == 'InvalidParameterValue':
#            print("Please check for missing SecurityGroup parameter")
#        else:
#            print(f"some other error occured {error}")
