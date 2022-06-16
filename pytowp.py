import requests
import json
import base64

user = 'admin'
pythonapp = '7Mwg CklO gDuh tzip fMyX SDYh'
url = 'http://website.local/wp-json/wp/v2'

data_string = user + ':' + pythonapp
token = base64.b64encode(data_string.encode())
headers = {'Authorization': 'Basic ' + token.decode('utf-8')}

f = open('openai-completed-description.txt', 'r')
content = f.read()

print(content)

post = {'title': 'Testgggg 1',
		'status': 'publish',
		'content': "jjjj",
		'author': '1',
		'format': 'standard'
		}

r = requests.post(url + '/posts', headers=headers, json=post)
print('Your post is published on ' + json.loads(r.content.decode('utf-8'))['link'])

