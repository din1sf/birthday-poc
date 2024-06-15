from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from birthday_utils import load_settings

def generate_birthday_wish(name):
    try:
        with open('prompt_birthday_wish.txt', 'r') as file:
            prompt = file.read()
    except FileNotFoundError:
        prompt = 'Happy Birthday {name}!'

    # treat prompt as a template and replace {name} with the actual name
    prompt = prompt.format(name=name)
    return generate('You are birthday wish generator', prompt, {'name': name})


def generate(system, user, params):
    settings = load_settings()
    # print('Loaded settings: ' + str(settings))
    api_key = settings['openai']['api-key']
    model = settings['openai']['model']
    print('Using OpenAI model: ' + model)

    llm = ChatOpenAI(openai_api_key=api_key, model=model)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("user", user)
    ])

    chain = prompt | llm 
    result = chain.invoke(params)
    return result.content

# print(generate_birthday_wish('Nikolay'))