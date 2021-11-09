import json
import boto3

def Stop_EC2():
    client = boto3.client('ec2')
    response = client.describe_instances(
        Filters=[
            {
                'Name':'tag:env',
                'Values':['dev']
            }
        ]
    )
    inst_list = []
    for Res in response['Reservations']:
        #loop thru all instances
        for inst in Res['Instances']:
            #print(inst['InstanceId'])
            
            #append to a list
            inst_list.append(inst['InstanceId'])
            client.stop_instances(InstanceIds=[inst['InstanceId']])
        #stop the instance
    return inst_list


def lambda_handler(event, context):
    # TODO implement
    list = Stop_EC2()
    return {
        'statusCode': 200,
        'body': json.dumps(list)
    }

