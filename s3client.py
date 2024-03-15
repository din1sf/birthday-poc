import boto3
from botocore.exceptions import NoCredentialsError

S3_BUCKET = 'birthday-poc'
S3_REGION = 'eu-central-1'

def upload_to_s3(local_file, bucket, s3_file, content_type='image/jpeg'):
    s3 = boto3.client('s3')
    link = f"https://{bucket}.s3.{S3_REGION}.amazonaws.com/{s3_file}"
    try:
        with open(local_file, 'rb') as file:   
            s3.put_object(Bucket=bucket, Key=s3_file, Body=file, ContentType=content_type)
        print(f"Upload Successful. File uploaded to {link}")
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")
    return link
    
def upload_birthday_card(file, target_file):
   return upload_to_s3(file, S3_BUCKET, target_file, 'image/jpeg')

def upload_birthday_page(file, target_file):
    return upload_to_s3(file, S3_BUCKET, target_file, 'text/html')

# upload_birthday_card('card.jpg', 'card.jpg')
# upload_birthday_page('card.html', 'card.html')