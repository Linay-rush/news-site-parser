import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import math

baseUrl = 'https://meduza.io'
response = requests.get(baseUrl)

main_parser = BeautifulSoup(response.text, features='html.parser')

header_menu = main_parser.select_one('nav.Header-menu')
categories = header_menu.select('a.Link-root')
for i in range(len(categories)):
    category = categories[i]
    text = category.text
    print(f'{i + 1}] {text}')

print('Select number of categories: ', end='')
numberOfCategory = int(input())

if numberOfCategory - 1 < 0 or numberOfCategory - 1 >= len(categories):
    print('Incorrect number of category')
    exit(-1)

category = categories[numberOfCategory - 1]
print(category.text)

url = f'https://meduza.io/api/w5/search?chrono={category}&page=0&per_page=24&locale=ru'

response = requests.get(url)

if response.status_code != 200:
    print('Error')
    exit(-1)
time1 = datetime.today()
time = datetime.timestamp(time1)
data = json.loads(response.text)
documents = data.setdefault('documents')

for key, value in documents.items():
    #document = documents[i].copy
    tmp = math.fabs(time - value['datetime'])
    if tmp <= 86400:
        title = value['title']
        url_second = value['url']
        print('https://meduza.io/' + url_second + ' ' + title)
print(data)
