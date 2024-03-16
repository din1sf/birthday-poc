import pandas as pd

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

    bd = next_birthday.strftime("%Y-%m-%d")
    if (days_until == 0):
       handle_birthday(name, row['email'], years, bd)
        
    # print('\nName: ' + name)
    # print('Birthday: ' + birthday)
    # print('Next birthday: ' + str(next_birthday))
    # print('Previous birthday: ' + str(prev_birthday))
    # print('Days until next birthday: ' + str(days_until))
    # print('Days after current birthday: ' + str(days_after))

print('Done')