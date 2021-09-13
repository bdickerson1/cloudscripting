import boto3
import json
import datetime

def defaultconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


s3 = boto3.client('s3')

#print(type(s3))

response = s3.list_buckets()

format_response = json.dumps(response, default=defaultconverter, indent=4)
#print(format_response)


for b_list in response['Buckets']:
    mybucket = b_list['Name']
    print(mybucket)
    
    object_response = s3.list_objects_v2(Bucket=mybucket)
    for obj in object_response['Contents']:
        print(obj['Key'])
      
