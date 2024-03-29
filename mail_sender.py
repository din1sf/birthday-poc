import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from birthday_utils import load_settings

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
            attachment_content_type = 'application/octet-stream'
            if attachment_path.endswith('.jpg'):
                attachment_content_type = 'jpeg'

            with open(attachment_path, 'rb') as f:
                part = MIMEApplication(f.read(), _subtype=attachment_content_type)
                part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))
                msg.attach(part)

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
        print("  Email sent to " + recipient)
    
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
        print("  Email sent! Message ID:", response['MessageId'])

def generate_birthday_email_content(name, card_link):
    try:
        with open('template_birthday_email.html', 'r', encoding='utf-8') as file:
            tmp = file.read()
    except FileNotFoundError:
        print('File not found')

    tmp = tmp.replace('{{name}}', name)
    tmp = tmp.replace('{{card}}', card_link)

    return tmp

def send_birthday_email(name, date, card_link, attachments, recipient):
    settings = load_settings()
    aws_access_key_id = settings['aws.ses']['aws-access-key-id']
    aws_secret_access_key = settings['aws.ses']['aws-secret-key']
    aws_region = settings['aws.ses']['region']
    sender = settings['aws.ses']['sender-email']

    subject = "Birthday reminder " + name + " " + date
    body_text = "Happy Birthday " + name
    body_html = generate_birthday_email_content(name, card_link)

    print('  Sending email to ' + recipient)
    send_email_with_attachment(aws_access_key_id, aws_secret_access_key, sender, recipient, aws_region, subject, body_text, body_html, attachments) 


# name = 'Eve'
# date = '2024-03-15'
# card_link = 'https://birthday-poc.s3.eu-central-1.amazonaws.com/index.html'
# attachments = ['cards/demo.jpg']
# send_birthday_email(name, date, card_link, attachments, '1153nikidimitrov@gmail.com')
# print('done')