import boto3

def CheckInstance():
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_instances()

    for Res in response['Reservations']:
        #loop thru all instances
        for inst in Res['Instances']:
            print(f"The EC2 instance ID is: {inst['InstanceId']}")
            
            #loop thru all security groups in the instance
            for sg in inst['SecurityGroups']:
                #call securitygroup function
                print(f"Checking security group {sg['GroupName']} for SSH access")
                sgSSH, sgSTUFF = CheckSecurityGroup(sg['GroupId'])
            
                #if return is true for SSH run revoke command
                if sgSSH == 1:                    
                    SSHvar = 22
                    print(f"Security Group {sg['GroupName']} has a rule {sgSTUFF} that allows SSH. Removing access to port 22 now")
                    resp = ec2_client.revoke_security_group_ingress(SecurityGroupRuleIds=[sgSTUFF],GroupId=sg['GroupId'])
                else:
                    print(f"Security Group {sg['GroupName']} doesn't have SSH allowed in")       
            #end sg loop
        #end inst loop
    #end Res loop

def CheckSecurityGroup(sg_id):
    SSHyes = 0
    sg_client = boto3.client('ec2')
    sg_response = sg_client.describe_security_group_rules(     
        Filters=[
            {   
                'Name': 'group-id',
                'Values': [sg_id,]
            },
        ],
    )
    #loop thru rules in each security group
    for rule in sg_response['SecurityGroupRules']:
        #check if port 22 is open
        if rule['ToPort'] == 22:
            value = rule['SecurityGroupRuleId']
            SSHyes = 1
        else:
            value = "nossh"
    #end rule loop    
    return SSHyes, value


def main():
    CheckInstance()

if __name__ == "__main__":
    main()