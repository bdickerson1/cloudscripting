import boto3
import json

s3 = boto3.client('s3')

bucket_name = 'week2-bucket-bdickerson1-ex2'

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
    'ErrorDocument': {'Key': 'error.html'},
    'IndexDocument': {'Suffix': 'index.html'},
    }
)
print(website_response)
index_file = open('index.html', 'rb')
s3.put_object(Body=index_file,Bucket=bucket_name,Key='index.html', ContentType='text/html')
index_file.close()

error_file = open('error.html', 'rb')
s3.put_object(Body=error_file,Bucket=bucket_name,Key='error.html', ContentType='text/html')
error_file.close()
