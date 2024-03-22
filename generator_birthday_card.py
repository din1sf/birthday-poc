from openai import OpenAI 
import requests
from birthday_utils import load_settings

def generate_birthday_card(name, filename='birthday_card.jpg'):
    try:
        with open('prompt_birthday_card.txt', 'r') as file:
            prompt = file.read()
    except FileNotFoundError:
        prompt = 'Happy Birthday {name}!'

    # treat prompt as a template and replace {name} with the actual name
    prompt = prompt.format(name=name)
    
    print('  Generating birthday card for: ' + name)
    image_url = generate_image(prompt)
    download_file(image_url, filename)

def generate_image(prompt):
    settings = load_settings()
    api_key = settings['openai']['api-key']
    image_model = settings['openai']['image-model']

    client = OpenAI(api_key=api_key)
    response = client.images.generate(
        model=image_model,
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    return image_url

def download_file(url, filename):
    print('  Downloading file: ' + filename)
    with open(filename, "wb") as file:
        response = requests.get(url)
        file.write(response.content)
    print('  File downloaded: ' + filename)


# generate_birthday_card('Pesho', 'cards/1.jpg')