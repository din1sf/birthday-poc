import base64

# generate image to base64 format
def image_to_Base64_format(filename):
    with open(filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode('utf-8')
    
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

def generate_birthday_html_message(name, card_file, wish):
    base64_image = image_to_Base64_format(card_file)

    try:
        # load the template from a file utf-8
        with open('birthday_message_template.html', 'r', encoding='utf-8') as file:
            tmp = file.read()
    except FileNotFoundError:
        tmp = default_message_template()

    image = 'data:image/jpeg;base64, {base64_image}'.format(base64_image=base64_image)
    tmp = tmp.replace('{{name}}', name)
    tmp = tmp.replace('{{message}}', wish)
    tmp = tmp.replace('{{image}}', image)

    return tmp

# html = generate_birthday_html_message('Nikolay', 'cards/birthday_card.jpg', 'Wishing you a great day!')
# # save the html to a file
# with open('birthday_message.html', 'w') as file:
#     file.write(html)
# print('Done')