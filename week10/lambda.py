import boto3

#from week10.lambda_stop_function import lambda_handler
import lambda_stop_function

#create lambda function to stop EC2 instances with tags 'env:dev'
def CreateLambda(f_name):
    client = boto3.client('iam')
    role_resp = client.get_role(RoleName='LabRole')
    #read in zip file
    handler = open('lambda_stop_function.zip', 'rb')
    scriptfile = handler.read()
    lam_client = boto3.client('lambda')
    #print(scriptfile)
    
    lam_response = lam_client.create_function(
        FunctionName=f_name,
        Role=role_resp['Role']['Arn'],
        Publish=True,
        PackageType="Zip",
        Runtime='python3.9',
        Code={'ZipFile':scriptfile},
        Handler='lambda_stop_function.lambda_handler'
    )
    return lam_response

#creat lambda function to START all EC2 instances
def CreateLambdaStart(f_name):
    client = boto3.client('iam')
    role_resp = client.get_role(RoleName='LabRole')
    #read in zip file
    handler = open('lambda_start_function.zip', 'rb')
    scriptfile = handler.read()
    lam_client = boto3.client('lambda')
    #print(scriptfile)
    
    lam_response = lam_client.create_function(
        FunctionName=f_name,
        Role=role_resp['Role']['Arn'],
        Publish=True,
        PackageType="Zip",
        Runtime='python3.9',
        Code={'ZipFile':scriptfile},
        Handler='lambda_start_function.lambda_handler'
    )
    return lam_response    

def InvokeLambda(f_name):
    lam_client = boto3.client('lambda')
    lamb_resp = lam_client.invoke(FunctionName=f_name)





def main():
    #check for lambda function
    fun_name = input("enter a name to create a EC2 stopping function: ")
    lam_client = boto3.client('lambda')
    response = lam_client.list_functions()
    
    #loop thru all Function names
    for Res in response['Functions']:
        if Res['FunctionName'] == fun_name:
            exists = 1
        else:
            noexists = 0

    #if function exists 
    if exists != 0:
        print(f"{fun_name} already exists")
        answer = input(f"would you like to invoke {fun_name} now? hit 'y' for YES ")
        if answer == 'y':
            InvokeLambda(fun_name)
            print(f"{fun_name} has been invoked. you're welcome.")
        else:
            print(f"not invoking {fun_name} right now")

    #if function doesn't exist, create it
    else:
        print(f"creating {fun_name} now")
        CreateLambda(fun_name)
        answer = input(f"would you like to invoke {fun_name} now? hit 'y' for YES ")
        if answer == 'y':
            InvokeLambda(fun_name)
            print(f"{fun_name} has been invoked. you're welcome.")
        else:
            print(f"not invoking {fun_name} right now")    

    start_instances = input("Would you like to create a function to start all EC2 instances?hit 'y' for YES ")
    if start_instances == 'y':
        fun_start = input('enter a name to create a EC2 stopping function: ')
        response2 = lam_client.list_functions()
        exists = 0

        #loop thru all Function names
        for Res in response2['Functions']:
            if Res['FunctionName'] == fun_start:
                exists = 1
            else:
                noexists = 0

        #if function exists 
        if exists != 0:
            print(f"{fun_start} already exists")
            answer = input(f"would you like to invoke {fun_start} now? hit 'y' for YES ")
            if answer == 'y':
                InvokeLambda(fun_start)
                print(f"{fun_start} has been invoked. you're welcome.")
            else:
                print(f"not invoking {fun_start} right now")

        #if function doesn't exist, create it
        else:
            print(f"creating {fun_start} now")
            CreateLambdaStart(fun_start)
            answer = input(f"would you like to invoke {fun_start} now? hit 'y' for YES ")
            if answer == 'y':
                InvokeLambda(fun_start)
                print(f"{fun_start} has been invoked. you're welcome.")
            else:
                print(f"not invoking {fun_start} right now")    
    else:
        print("not creating a function to start EC2.")


if __name__ == "__main__":
    main()