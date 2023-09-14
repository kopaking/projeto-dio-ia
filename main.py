from dotenv import load_dotenv
import json
import pandas as pd
import requests
import time
import openai
import os

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")
df = pd.read_csv('SDW2023.csv')
user_ids = df['UserID'].tolist()
sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'

def get_user(id):
    response = requests.get(f'{sdw2023_api_url}/users/{id}')
    return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]
print(f'json.dumps(users, indent=2) = {json.dumps(users, indent=2)}')
nome = user['name'].capitalize()

def generate_ai_news():
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "Você é um especialista em marketing bancário."
        },
        {
            "role": "user",
            "content": f"Crie uma mensagem para {nome} sobre a importância dos investimentos (máximo de 100 caracteres)"
        }
    ]
    )
    return completion.choices[0].message.content.strip('\"')

for user in users:
    news = generate_ai_news()
    print(f'news = {news}')
    user['news'].append({
        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
        "description": news
    })
    time.sleep(1)

def update_user(user):
    response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
    return True if response.status_code == 200 else False

for user in users:
    success = update_user(user)
    print(f"User {nome} updated? {success}!")
     