import requests
from bs4 import BeautifulSoup

baseUrl = 'https://meduza.io'
response = requests.get(baseUrl)

main_parser = BeautifulSoup(response.text, features = 'html.parser')

header_menu = main_parser.select_one('nav.Header-menu')
categories = header_menu.select('a.Link-root')
print(categories)
