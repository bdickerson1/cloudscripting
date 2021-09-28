from os import write
import boto3
import json
import csv

DRYRUN = False

def Get_Instances(key,value):
    ec2vm = boto3.client('ec2')
    paginator = ec2vm.get_paginator('describe_instances')
    page_list = paginator.paginate(
        Filters=[
            {
                'Name':key,
                'Values':[value]
            },
        ]
    )
    response = []
    for page in page_list:
        for reservation in page['Reservations']:
            response.append(reservation)
    #response = ec2vm.describe_instances()
    return response

def CSV_Writer(header,content):
    hFile = open('export.csv', 'w')
    writer = csv.DictWriter(hFile,fieldnames=header)
    writer.writeheader()
    for line in content:
        writer.writerow(line)
    hFile.close()

def main():
    reservation = Get_Instances('instance-type','t2.micro')
    header = ['InstanceId','InstanceType','State','PublicIpAddress','Monitoring']
    content = []
    for entry in reservation:
        #print(f"Adding instance {entry['Instances'][0]['InstanceId']}")
        content.append(
            {
                "InstanceId": entry['Instances'][0]['InstanceId'],
                "InstanceType": entry['Instances'][0]['InstanceType'],
                "State": entry['Instances'][0]['State']['Name'],
                "PublicIpAddress": entry['Instances'][0].get('PublicIpAddress',"N/A"),
                "Monitoring": entry['Instances'][0]['Monitoring']['State']
            }
        )
    CSV_Writer(header,content)

if __name__ == "__main__":
    main()
