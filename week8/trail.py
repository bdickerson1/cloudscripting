import boto3
import s3enforce
import json

#get account info
sts_client = boto3.client("sts")
account_id = sts_client.get_caller_identity()["Account"]


#bucket_name = input("Enter a unique bucket name to create and log CloudTrail to: ")
bucket_name = ""


#set a bucket policy


#create a CloudTrail
def CreateTrail(b_name, t_name):
    c_trail = boto3.client("cloudtrail")
    response = c_trail.create_trail(Name=t_name,S3BucketName=b_name)
    c_trail.start_logging(Name=t_name)
    return response


def main():
    #bucket_name = input("Enter a unique bucket name to create and log CloudTrail to: ")
    makebucket = s3enforce.CreateBucket(bucket_name)
    
    buck_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AWSCloudTrailAclCheck20150319",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "s3:GetBucketAcl",
                "Resource": f"arn:aws:s3:::{makebucket}"
            },
            {
                "Sid": "AWSCloudTrailWrite20150319",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "s3:PutObject",
                "Resource": f"arn:aws:s3:::{makebucket}/AWSLogs/{account_id}/*",
                "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}
            }
        ]
    }
    
    bucket_policy = s3enforce.SetBucketPolicy(makebucket,json.dumps(buck_policy, indent=4))
    
    #s3enforce.SetBucketPolicy(makebucket,bucket_policy)
    trail_name = input("Enter a CloudTrail name: ")
    t_response = CreateTrail(makebucket, trail_name)
    #print(t_response)

    
if __name__ == "__main__":
    main()