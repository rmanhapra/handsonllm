import json
import os
from urllib import response
from dotenv import load_dotenv
from utilities.scraper import fetch_website_contents, fetch_website_links
from IPython.display import display, Markdown,update_display
from openai import OpenAI

system_prompt = """
you are a designer. you are given a list of links to websites. 
you will analyze the contents of each website, you have to make sure the 
relevance of the links that can be put in brochure of a company
ex: About, Leadership etc and return only the relevant links.

The response format must be of JSON as below
{
    
  "relevant_links": [{type: "Relevant Link 1", "url": "https://example.com/relevant-link1"},
                    {type: "Relevant Link 2", "url": "https://example.com/re
levant-link2"}]
}
"""

def getUserPrompt(url):
    user_prompt = f"""
    you are given a list of links to website {url}.
    you will analyze the contents of each website, you have to make sure the
relevance of the links and its content the {url} that can be put in brochure of a company
    """
    links = fetch_website_links(url);
    print (f"Base Links for {url}: {links}")
    return user_prompt + "\n\n".join(links)

def select_relevant_links(url):
    load_dotenv(override=True)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY is not set in the environment variables.")
    
    openai = OpenAI()
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": getUserPrompt(url)}
    ]
   
    
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format={
            "type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

def linkandpagecontent(url):
    contents = fetch_website_contents(url)
    results = f'''## Landing Page:\n\n#### {contents} '''
       
    links = select_relevant_links(url)
    print (f"Relevant links for {url}: {links}")
    for link in links["relevant_links"]:
        try:
            content = fetch_website_contents(link['url'])
            results += f"\n\n## {link['type']}:\n\n#### {content}"
        except Exception as e:
            print(f"Error fetching content for {link}: {e}")
    return results


def brochure_generator(name,url,isStreaming):
    contents = linkandpagecontent(url)
    system_prompt = f"""you are a brochure designer.
    you will be provided with sections of a brochure with its content.You have to 
     generate a nice brochure that can be sent to enterprise companies. Generate response in markdown format"""
    
    user_prompt = f"""
    Here is the companay {name} and its content {contents}. Generate a nice 
    brochure that can be sent to enterprise companies."""

    load_dotenv(override=True)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY is not set in the environment variables.") 
    
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    if not isStreaming:
        printContent(messages)
    else:
        streamContent(messages)
   

def printContent(messages):
    openai = OpenAI()
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    content = response.choices[0].message.content
    print (content)
    display(Markdown(content))

def streamContent(messages): 
    openai = OpenAI()
    stream = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True
    )
    response = ""
    display_handle = display(Markdown(""), display_id=True)
    for chunk in stream:
       response += chunk.choices[0].delta.content or ""
       update_display(Markdown(response), display_id=display_handle.display_id)
    print("Streaming completed.")