
import boto3
from pprint import pprint
client = boto3.client("s3")
Bucket = input("Enter the bucket name: ")
IP = input('Enter the IP address: ')

# creating bucket
response = client.create_bucket(Bucket=Bucket)
print(f"Your bucket: {Bucket} is created successfully!")

# attaching bucket policy
policy_json = f'''{{
    "Version": "2012-10-17",
    "Statement": [
        {{
            "Action": "s3:*",
            "Effect": "Allow",
            "Resource": "arn:aws:s3:::{Bucket}/*",
            "Condition": {{
                "IpAddress": {{
                    "aws:SourceIp": "{IP}/24"
                }}
            }},
            "Principal": "*"
        }}
    ]
}}'''

response = client.put_bucket_policy(
    Bucket=Bucket,
    Policy=policy_json
)
print(f"Bucket policy is attached to the bucket: {Bucket}")

# adding lifycle rules
response = client.put_bucket_lifecycle_configuration(
    Bucket=Bucket,
    LifecycleConfiguration={
        'Rules': [
            {
                'Expiration': {
                    'Days': 14,
                },
                'Filter': {
                    'Prefix': '/',
                },
                'ID': 'DeleteAfter14Days',
                'Status': 'Enabled'
            }
        ]
    }
)
print(f"Lifecycle rule is attached to the bucket: {Bucket}")
