import json
import boto3

def Start_EC2():
    client = boto3.client('ec2')
    response = client.describe_instances(
#        Filters=[
#            {
#                'Name':'tag:env',
#                'Values':['dev']
#            }
#        ]
    )
    inst_list = []
    for Res in response['Reservations']:
        #loop thru all instances
        for inst in Res['Instances']:
            #print(inst['InstanceId'])
            
            #append to a list
            inst_list.append(inst['InstanceId'])
            client.start_instances(InstanceIds=[inst['InstanceId']])
        #stop the instance
    return inst_list


def lambda_handler(event, context):
    # TODO implement
    list = Start_EC2()
    return {
        'statusCode': 200,
        'body': json.dumps(list)
    }

