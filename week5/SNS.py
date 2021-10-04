import boto3
from botocore.parsers import ResponseParser

def CreateSNSTopic(t_name):
    sns_client = boto3.client('sns')
    response = sns_client.create_topic(Name=t_name)
    return response["TopicArn"]

def SubscribeEmail(ARN,email):
    email_client = boto3.client('sns')
    response = email_client.subscribe(TopicArn=ARN,Protocol='email',Endpoint=email)
    return response["SubscriptionArn"]
