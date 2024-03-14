from openai import OpenAI 
import requests
import os

def generate_birthday_card(name, filename='birthday_card.jpg'):
    try:
        with open('birthday_card_prompt.txt', 'r') as file:
            prompt = file.read()
    except FileNotFoundError:
        prompt = 'Happy Birthday {name}!'

    # treat prompt as a template and replace {name} with the actual name
    prompt = prompt.format(name=name)
    
    print('generating birthday card for: ' + name)
    image_url = generate_image(prompt)
    download_file(image_url, filename)

def generate_image(prompt):
    client = OpenAI()
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    return image_url

def download_file(url, filename):
    print('downloading file: ' + filename + ' from ' + url)
    # ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "wb") as file:
        response = requests.get(url)
        file.write(response.content)
    print('file downloaded: ' + filename)


# generate_birthday_card('Nikolay', 'cards/card.jpg')