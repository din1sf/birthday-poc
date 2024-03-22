import boto3
from botocore.exceptions import NoCredentialsError
from birthday_utils import load_settings

def upload_to_s3(local_file, aws_access_key_id, aws_secret_access_key, region, bucket, s3_file, content_type='image/jpeg'):
    # create s3 client with specific key and secret
    s3 = boto3.client('s3', region_name=region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    link = f"https://{bucket}.s3.{region}.amazonaws.com/{s3_file}"
    try:
        with open(local_file, 'rb') as file:   
            s3.put_object(Bucket=bucket, Key=s3_file, Body=file, ContentType=content_type)
        print(f"  Upload Successful. File uploaded to {link}")
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")
    return link
    

def upload(file, target_file, content_type):
    settings = load_settings()
    aws_access_key_id = settings['aws.s3']['aws-access-key-id']
    aws_secret_access_key = settings['aws.s3']['aws-secret-key']
    aws_region = settings['aws.s3']['region']
    bucket = settings['aws.s3']['bucket-name']
    return upload_to_s3(file, aws_access_key_id, aws_secret_access_key, aws_region, bucket, target_file, content_type)

def download_from_s3(aws_access_key_id, aws_secret_access_key, region, bucket, s3_file, local_file):
    s3 = boto3.client('s3', region_name=region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    try:
        s3.download_file(bucket, s3_file, local_file)
        print(f"  Download Successful. File downloaded to {local_file}")
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")
    return local_file

def download(file, target_file):
    settings = load_settings()
    aws_access_key_id = settings['aws.s3']['aws-access-key-id']
    aws_secret_access_key = settings['aws.s3']['aws-secret-key']
    aws_region = settings['aws.s3']['region']
    bucket = settings['aws.s3']['bucket-name']
    return download_from_s3(aws_access_key_id, aws_secret_access_key, aws_region, bucket, file, target_file)

def upload_birthday_card(file, target_file):
    return upload(file, target_file, 'image/jpeg')

def upload_birthday_page(file, target_file):
    return upload(file, target_file, 'text/html')

def download_birthdays_cvs(file='birthdays.csv'):
    return download(file, 'remote-birthdays.csv')

# upload_birthday_card('card.jpg', 'card.jpg')
# upload_birthday_page('cards/demo.html', 'index.html')
# download_birthdays_cvs()