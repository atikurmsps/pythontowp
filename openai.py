import openai
import base64
import json
import requests

openai.api_key = 'API HERE'

url = 'http://aiblogtest.local'
username = 'admin'
app_pass = '7Mwg CklO gDuh tzip fMyX SDYh'

#OpenAI completes your keywords
def grab_completed_text(stext):
        response = openai.Completion.create(
          engine="text-davinci-002",
          prompt=stext,
          temperature=0.7,
          max_tokens=500,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )
        return response['choices'][0]['text']

# stores queries here
chosen_keywords = []

# opens the people-also-ask.txt file to read the quesitons
file_open_paan = open('people-also-ask.txt', 'r')
chosen_keywords = file_open_paan.read().splitlines()
original_keyword_untrimmed = chosen_keywords[0].split(' ')
original_keyword =  " ".join(original_keyword_untrimmed[1:])
chosen_keywords.pop(0)

#removes previous texts from the file 'openai-completed-descriptions.txt'
open('openai-completed-description.txt', 'w').close()

# completes the introduction query
introduction_query = "Write an introductory processional article "  + original_keyword
processed_keyword =  introduction_query + original_keyword
openai_completed_introduction =  grab_completed_text(processed_keyword)
file_open = open("openai-completed-description.txt", 'a')
file_open.write(f'<p>{openai_completed_introduction}</p>\n')
file_open.write("\n")
file_open.close()

# completes people-also-ask queries
for keyword in chosen_keywords:
    completed_text = grab_completed_text(keyword)
    file_open = open("openai-completed-description.txt", 'a')
    file_open.write(f'<h2>{keyword}</h2>\n')
    file_open.write(f'<p>{completed_text}</p>\n')
    file_open.write("\n")

# completes the conclusion query
conclusion_query = "Write an article conclusion about "  + original_keyword
processed_keyword =  conclusion_query + original_keyword
openai_completed_introduction =  grab_completed_text(processed_keyword)
file_open = open("openai-completed-description.txt", 'a')
file_open.write("<h2>Conclusion</h2>\n")
file_open.write(f'<p>{openai_completed_introduction}</p>')
file_open.write("\n")

with open('openai-completed-description.txt', 'r') as file:
    content = file.read()

    auth = f'{username}:{app_pass}'
    token = base64.b64encode(auth.encode())
    headers = {
            'Authorization': f'Basic {token.decode("utf-8")}',
            'Content-Type': 'application/json'
        }
    res = requests.post(
            url + '/wp-json/wp/v2/posts',
            headers=headers,
            json={
                'title': original_keyword,
                'status': 'draft',
                'content': content,
                'author': 1,
                'format': 'standard'
            }
        )
    print(original_keyword)
