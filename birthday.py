import pandas as pd
import boto3
from botocore.exceptions import NoCredentialsError
from birthday_card_generator import *
from birthday_wish_generator import *
from birtday_message_generator import *
from mail_sender import *

def upload_to_s3(local_file, bucket, s3_file):
    s3 = boto3.client('s3')

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print(f"Upload Successful. File uploaded to https://{bucket}.s3.amazonaws.com/{s3_file}")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    
def upload_birthday_file(file):
    target_file = file.split('/')[1]
    upload_to_s3(file, 'birthday-poc', target_file)


def handle_birthday(name, email, years):
    print('\r\nHappy ' + years + ' Birthday '+ name)

    # current year as string
    current_year = str(pd.to_datetime('today').year)
    filename_prefix = current_year + '-birthday-' + name

    birthday_card_file = 'cards/' + filename_prefix + '.jpg'
    birthday_message_file = 'cards/' + filename_prefix + '.html'

    generate_birthday_card(name, birthday_card_file)    

    birthday_wish = generate_birthday_wish(name)

    html_message = generate_birthday_html_message(name, birthday_card_file, birthday_wish)
    with open(birthday_message_file, 'w') as file:
        file.write(html_message)

    upload_birthday_file(birthday_card_file)
    upload_birthday_file(birthday_message_file)

    send_birthday_email(name, html_message, [birthday_card_file, birthday_message_file])

        
# read the CSV file
print('Reading birthdays.csv')
df = pd.read_csv('birthdays.csv',delimiter=';')
print(df)

# iterate over the rows of the DataFrame
for index, row in df.iterrows():
    birthday = row['birthday']
    name = row['name']
    now = pd.to_datetime('today').normalize()

    # calculate the number of days until the next birthday
    next_birthday = pd.to_datetime(birthday).replace(year=now.year)
    prev_birthday = next_birthday
    if now > next_birthday:
        next_birthday = next_birthday.replace(year=now.year + 1)
    days_until = (next_birthday - now).days
    days_after = (now - prev_birthday).days
    years = str(now.year - pd.to_datetime(birthday).year)

    if (days_until == 0):
       handle_birthday(name, row['email'], years)
        
    # print('\nName: ' + name)
    # print('Birthday: ' + birthday)
    # print('Next birthday: ' + str(next_birthday))
    # print('Previous birthday: ' + str(prev_birthday))
    # print('Days until next birthday: ' + str(days_until))
    # print('Days after current birthday: ' + str(days_after))

print('Done')