import os
from dotenv import load_dotenv
from openai import OpenAI
import ast

load_dotenv()
api_key= os.getenv("OPENAI_APIKEY")
client = OpenAI(api_key=api_key)


# list_a = string1.split("•")
# if list_a[0] == '':
#     list_a.remove('')
# list_a = [string[:-1] for string in list_a]
# print(list_a)

def generate_keyword(topic_name, requirement):
    prompt = f"here are two key phrases:{topic_name} and {requirement}, you are to combine them into something short without losing its meaning.only add relevant words. a max of 10 words"

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "your role is to optimise youtube searches when given a keywords"},
        {"role": "user", "content": prompt}
    ]
    )

    chatgpt_output = completion.choices[0].message.content
   
    return chatgpt_output











   







