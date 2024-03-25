import pandas as pd
import argparse
from datetime import datetime
from generator_birthday_card import *
from generator_birthday_wish import *
from generator_birthday_page import *
from mail_sender import *
from s3client import *

def handle_birthday(name, email, years, birthday):
    print('\r\nHappy ' + years + ' Birthday '+ name)

    # current year as string
    current_year = str(pd.to_datetime('today').year)
    filename_prefix = current_year + '-birthday-' + name

    birthday_card_filename = filename_prefix + '.jpg'
    birthday_page_filename = filename_prefix + '.html'

    birthday_card_file = 'cards/' + birthday_card_filename
    birthday_page_file = 'cards/' + birthday_page_filename

    generate_birthday_card(name, birthday_card_file)    

    birthday_wish = generate_birthday_wish(name)

    html_message = generate_birthday_html_page(name, birthday_card_filename, birthday_wish)
    with open(birthday_page_file, 'w') as file:
        file.write(html_message)

    birthday_card_link = upload_birthday_card(birthday_card_file, birthday_card_filename)
    birthday_page_link = upload_birthday_page(birthday_page_file, birthday_page_filename)

    card_link = birthday_page_link
    attachments = [birthday_card_file]
    send_birthday_email(name, birthday, card_link, attachments, email)
       
def handle_birthday_file(file):
    print('Reading ' + file)
    df = pd.read_csv(file, delimiter=';')
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

        # format dd month yyyy
        bd = next_birthday.strftime("%d %B %Y")
        if (days_until >0 and days_until < 14):
            print('\r\nBirthday reminder: ' + name + ' in ' + str(days_until) + ' days')
        if (days_until == 0):
            handle_birthday(name, row['email'], years, bd)
            
        # print('\nName: ' + name)
        # print('Birthday: ' + birthday)
        # print('Next birthday: ' + str(next_birthday))
        # print('Previous birthday: ' + str(prev_birthday))
        # print('Days until next birthday: ' + str(days_until))
        # print('Days after current birthday: ' + str(days_after))

    print('Done')


# print current time

print('Running on ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
file='birthdays.csv'
remote = False

parser=argparse.ArgumentParser(description="Birthday reminder tool")
parser.add_argument("--remote", help="Download birthdays from S3 bucket", action='store_true')
parser.add_argument("--file", help="CSV file with birthdays")
args=parser.parse_args()

if args.file:
   file = args.file

if args.remote:
    remote = True

if remote:
    print('Downloading birthdays from S3 bucket. File: ' + file)
    download_birthdays_cvs(file)
    file = 'remote-birthdays.csv'

handle_birthday_file(file)
