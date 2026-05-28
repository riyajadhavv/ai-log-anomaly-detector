import boto3
import json
import argparse
from datetime import datetime

def list_instances(region='ap-south-1'):
    """List all EC2 instances and their states."""
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_instances()
    
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            name = ''
            for tag in instance.get('Tags', []):
                if tag['Key'] == 'Name':
                    name = tag['Value']
            instances.append({
                'id': instance['InstanceId'],
                'name': name,
                'type': instance['InstanceType'],
                'state': instance['State']['Name'],
                'public_ip': instance.get('PublicIpAddress', 'N/A')
            })
    return instances

def start_instance(instance_id, region='ap-south-1'):
    """Start a stopped EC2 instance."""
    ec2 = boto3.client('ec2', region_name=region)
    ec2.start_instances(InstanceIds=[instance_id])
    print(f"Starting instance {instance_id}...")

def stop_instance(instance_id, region='ap-south-1'):
    """Stop a running EC2 instance."""
    ec2 = boto3.client('ec2', region_name=region)
    ec2.stop_instances(InstanceIds=[instance_id])
    print(f"Stopping instance {instance_id}...")

def create_s3_bucket(bucket_name, region='ap-south-1'):
    """Create an S3 bucket with versioning enabled."""
    s3 = boto3.client('s3', region_name=region)
    s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={'LocationConstraint': region}
    )
    # Enable versioning
    s3.put_bucket_versioning(
        Bucket=bucket_name,
        VersioningConfiguration={'Status': 'Enabled'}
    )
    print(f"Bucket {bucket_name} created with versioning enabled.")

def audit_iam_users():
    """List all IAM users and their last activity."""
    iam = boto3.client('iam')
    response = iam.list_users()
    
    report = []
    for user in response['Users']:
        report.append({
            'username': user['UserName'],
            'created': str(user['CreateDate']),
            'last_used': str(user.get('PasswordLastUsed', 'Never'))
        })
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    with open(f'iam_audit_{timestamp}.json', 'w') as f:
        json.dump(report, f, indent=2)
    print(f"IAM audit saved to iam_audit_{timestamp}.json")
    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AWS Infrastructure Automation')
    parser.add_argument('--action', choices=['list', 'start', 'stop', 'create-bucket', 'iam-audit'], required=True)
    parser.add_argument('--instance-id', help='EC2 Instance ID')
    parser.add_argument('--bucket', help='S3 Bucket name')
    parser.add_argument('--region', default='ap-south-1')
    args = parser.parse_args()

    if args.action == 'list':
        instances = list_instances(args.region)
        for i in instances:
            print(f"{i['id']} | {i['name']} | {i['type']} | {i['state']} | {i['public_ip']}")
    elif args.action == 'start' and args.instance_id:
        start_instance(args.instance_id, args.region)
    elif args.action == 'stop' and args.instance_id:
        stop_instance(args.instance_id, args.region)
    elif args.action == 'create-bucket' and args.bucket:
        create_s3_bucket(args.bucket, args.region)
    elif args.action == 'iam-audit':
        audit_iam_users()
