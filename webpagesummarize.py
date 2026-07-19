import os
from dotenv import load_dotenv
from utilities.scraper import fetch_website_contents
#from IPython.display import display, Markdown
from openai import OpenAI

system_prompt = """
You are a journalist that analyzes the contents of a website,
and provides a short, snarky, humorous summary, ignoring text that might be navigation related.
Respond in markdown. Do not wrap the markdown in a code block - respond just with the markdown.
"""
user_prompt_prefix = """Here are the contents of a website.
Provide a short summary of this website.
If it includes news or announcements, then summarize these too. """

load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY is not set in the environment variables.")
        

def openaitest():
    
    messsage = "Hey!! Tell me a motivation quote for today."
    messages = [{"role": "user", "content": messsage}]

    openai = OpenAI()
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages)
    print(response.choices[0].message.content)

def scrapertest():
    url = "https://edwarddonner.com"
    title_and_content =fetch_website_contents(url)
    print(title_and_content)

def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_prefix + website}
    ]

def summarize_website(website):
    openai = OpenAI()
    messages = messages_for(fetch_website_contents(website))
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return response.choices[0].message.content

def summarize_website_ollama(website):
    openai = OpenAI(base_url="http://localhost:11434/v1",api_key="ollama")
    messages = messages_for(fetch_website_contents(website))
    response = openai.chat.completions.create(
        model="gemma3:270m",
        messages=messages
    )
    return response.choices[0].message.content
 



