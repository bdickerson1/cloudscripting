import boto3
import datetime
import pytz

IAM = boto3.client('iam')
response = IAM.list_roles()
role_list = response['Roles']

for key in role_list:
    c_date = key['CreateDate']
    r_name = key['RoleName']
    if c_date > (pytz.utc.localize(datetime.datetime.utcnow())-datetime.timedelta(days=90)):
        print(key['RoleName']," ",key['CreateDate'])
        policy = IAM.list_role_policies(RoleName=r_name)
        if policy['PolicyNames'] == "":
            print(f"no policy exists")
        else:
            print(policy['PolicyNames'])
    else:
        print(f"{key['RoleName']}, is older than 90 days")


