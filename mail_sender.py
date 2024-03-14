import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import pandas as pd
import os
import base64

def send_email_with_attachment(aws_access_key_id, aws_secret_access_key, sender, recipient, aws_region, subject, body_text, body_html, attachments):
    # Create a new SES client
    client = boto3.client(
        'ses',
        region_name=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    # Create a multipart/mixed parent container
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    # Create a multipart/alternative child container
    msg_body = MIMEMultipart('alternative')

    # Attach the text and HTML versions of the message
    textpart = MIMEText(body_text, 'plain')
    htmlpart = MIMEText(body_html, 'html')
    msg_body.attach(textpart)
    msg_body.attach(htmlpart)

    # Attach the multipart/alternative child container to the multipart/mixed parent container
    msg.attach(msg_body)

    # iterate over attachments
    for attachment in attachments:
        attachment_path = attachment
        if attachment_path:
            with open(attachment_path, 'rb') as f:
                part = MIMEApplication(f.read())
                part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))
                msg.attach(part)

    # if attachment_path:
    #     with open(attachment_path, 'rb') as f:
    #         part = MIMEApplication(f.read())
    #         part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))
    #         msg.attach(part)

    # Convert the message to a string and send
    try:
        response = client.send_raw_email(
            Source=sender,
            Destinations=[recipient],
            RawMessage={
                'Data': msg.as_string(),
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:", response['MessageId'])



    
def send_email(aws_access_key_id, aws_secret_access_key, sender, recipient, aws_region, subject, body_text, body_html):
    # Create a new SES client
    client = boto3.client(
        'ses',
        region_name=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    
    # Try to send the email
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [recipient],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': body_html,
                    },
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': subject,
                },
            },
            Source=sender,
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:", response['MessageId'])

def send_birthday_email(name, html, card):
    df = pd.read_csv('ses-smtp-user.csv')

    aws_access_key_id = df['Access key ID'][0]
    aws_secret_access_key = df['Secret access key'][0]
    aws_region = 'eu-central-1'

    sender = '1153nikidimitrov@gmail.com'
    recipient = '1153nikidimitrov@gmail.com'
    subject = "Happy Birthday " + name
    body_text = "Happy Birthday " + name
    body_html = html

    # send_email(aws_access_key_id, aws_secret_access_key, sender, recipient, aws_region, subject, body_text, body_html)
    send_email_with_attachment(aws_access_key_id, aws_secret_access_key, sender, recipient, aws_region, subject, body_text, body_html, card) 


    
# send_birthday_email('Nikolay', 'happy birthday', ['_cards/2024-birthday-Nikolay.jpg', '_cards/2024-birthday-Nikolay.html'])
# print('done')