import boto3
import argparse
import string
import random

s3 = boto3.client('s3')
#bucket_name = 'week8-bucket-bdickerson1'



#create a bucket with provided name
def CreateBucket(b_name):
    s3 = boto3.client('s3')
    b_name = input("Enter a unique name to create an S3 bucket: ")
    response = s3.create_bucket(Bucket=b_name)
    return b_name

#delete a bucket with provided name
def DeleteBucket(b_name):
    s3 = boto3.client('s3')
    response = s3.delete_bucket(Bucket=b_name)
    return response

#encrypts a bucket with provided name
def EnforceS3Encryption(b_name):
    s3 = boto3.client('s3')
    response = s3.put_bucket_encryption(Bucket = b_name, 
    ServerSideEncryptionConfiguration={
        'Rules': [
            {
                'ApplyServerSideEncryptionByDefault':{
                'SSEAlgorithm':'AES256'
                }
            }
        ]
    }
)

#applies a policy to an S3 bucket
def SetBucketPolicy(b_name,b_policy):
    s3 = boto3.client('s3')
    policy_response = s3.put_bucket_policy(Bucket=b_name,Policy=b_policy)
    return policy_response

def main():
    #bucket_name = input("Enter a unique bucket name to create: ")
    bucket_name = ""
    makebucket = CreateBucket(bucket_name)
    #del_buck_name = input("Enter a unique bucket name to delete: ")
    #del_bucket = DeleteBucket(del_buck_name)
    encrypt_bucket = input("Enter a bucket name to encrypt: ")
    EnforceS3Encryption(encrypt_bucket)

if __name__ == "__main__":
    main()