import boto3
import argparse

# this script will take in an user group name and tell return whether it exists or not

IAM = boto3.client('iam')
response = IAM.list_groups()

parser = argparse.ArgumentParser(description="This is to allow arguments")
parser.add_argument('-g',dest='group_name', type=str, required=True)

args = parser.parse_args()
g_name = args.group_name
group_list = response['Groups']

# this loops through all the groups and compares the entered name to the existing group names
# counter to print if the group doesn't exist
exists = 0

for name in group_list:
    name1 = (name['GroupName'])
    

    #this if statement does the comparing of strings
    if name1 == g_name:
        print("That group already exists")
        exists = 1
    else:
        print("")

# this checks if the exists varible was incremented and prints out a statement if it wasn't
if exists == 0:
    print("That group doesn't exist")




    
