import boto3
import argparse

ec2_client = boto3.client('ec2')
response = ec2_client.describe_security_groups()
parser = argparse.ArgumentParser(description="This is to allow arguments")
parser.add_argument('-sg',dest='group_name', type=str)
args = parser.parse_args()
g_name = args.group_name
nothing = 0

if not args.group_name:
    for gr_name in response['SecurityGroups']:
        #print(gr_name['IpPermissions'])
        for ingress in gr_name['IpPermissions']:
            #print(ingress['IpRanges'])
            for cidr in ingress['IpRanges']:
                print(f"Security Group {gr_name['GroupName']} allows access from {cidr['CidrIp']}")
                if cidr['CidrIp'] == '0.0.0.0/0' or cidr['CidrIp'] == '0.0.0.0':
                    print(f"{gr_name['GroupName']} is open to the public internet")
                else:
                    nothing = 1
else:
    for gr_name in response['SecurityGroups']:
        if g_name == gr_name['GroupName']:
            nothing = 1
            for ingress in gr_name['IpPermissions']:
                for cidr in ingress['IpRanges']:
                    print(f"Security Group {gr_name['GroupName']} allows access from {cidr['CidrIp']}")
                    if cidr['CidrIp'] == '0.0.0.0/0' or cidr['CidrIp'] == '0.0.0.0':
                        #print(cidr['CidrIp'])
                        print(f"{gr_name['GroupName']} is open to the public internet")
                    else:
                        #print(f"{gr_name['GroupName']} is not open to the internet")
                        whatever = 1

        else:
            whatever = 1
            #print("That security group doesn't exist, please double check your entry")

if nothing ==  0:
    print("That security group doesn't exist, please double check your entry")
