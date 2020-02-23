import requests
from bs4 import BeautifulSoup

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

url = baseUrl + category['href']
print(url)
