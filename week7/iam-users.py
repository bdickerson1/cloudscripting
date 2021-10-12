import boto3
import argparse

IAM = boto3.client('iam')
response = IAM.list_users()
parser = argparse.ArgumentParser(description="This is to allow arguments")
parser.add_argument('-u',dest='user_name', type=str, required=True)

args = parser.parse_args()
u_name = args.user_name

user_list = response['Users']

user_exists = 0

for name in user_list:
    #print(name['UserName'])
    name1 = (name['UserName'])
    if name1 == u_name:
        user_exists = 1
        #print("that user exists")
    else:
        #this does nothing
        stuff = 1
    
if user_exists == 0:
    print("user doesn't exist")
else:
    print("that user exists")
