
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

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
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if openai_api_key is None:
        raise ValueError("OpenAI API key is not set in the environment variable OPENAI_API_KEY")
    llm = ChatOpenAI(openai_api_key=openai_api_key)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("user", user)
    ])

    chain = prompt | llm 
    result = chain.invoke(params)
    return result.content

# print(generate_birthday_wish('Nikolay'))