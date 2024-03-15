
def default_message_template(): 
    return """<html>
    <head></head>
    <body>
    <h1>Happy birthday {{name}}</h1>
    <p>{{wish}}</p>
    <img src="{{image}}" alt="Image" /> 
    </body>
    </html>
    """

def generate_birthday_html_page(name, card_file_name, wish):
    try:
        # load the template from a file utf-8
        with open('birthday_message_template.html', 'r', encoding='utf-8') as file:
            tmp = file.read()
    except FileNotFoundError:
        tmp = default_message_template()

    image = card_file_name
    tmp = tmp.replace('{{name}}', name)
    tmp = tmp.replace('{{message}}', wish)
    tmp = tmp.replace('{{image}}', image)

    return tmp

# html = generate_birthday_html_message('Nikolay', 'cards/birthday_card.jpg', 'Wishing you a great day!')
# # save the html to a file
# with open('birthday_message.html', 'w') as file:
#     file.write(html)
# print('Done')