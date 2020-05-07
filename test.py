import requests
from bs4 import BeautifulSoup
from datetime import datetime

response = requests.get('https://lenta.ru')

time_now = datetime.timestamp(datetime.today())

main_parser = BeautifulSoup(response.text, features='html.parser')
sidebar_menu = main_parser.select_one('ul.b-sidebar-menu__list')
headers = sidebar_menu.select('li.b-sidebar-menu__list-item')
for i in range(len(headers)-1):
    header = headers[i]
    text = header.text
    print(f'{i+1}] {text}')
print('15] Последние новости')
print('Select number of categories', end = '')
header_number = int(input())

if 0<=header_number - 1<len(headers)-1:
     header = headers[header_number - 1]
     print(header.text)

     a = header.select_one('a')
     url = a['href']

     response = requests.get('https://lenta.ru' + url)

     second_parser = BeautifulSoup(response.text, features='html.parser')

     contents = second_parser.select('div.b-tabloid__topic_news')
     for content in contents:
         try:
             date = content.select_one('div.g-date')
             time = date.text
             conteiner = content.select_one('div.titles')
             a2 = conteiner.select_one('a')
             url2 = a2['href']
             date1 = url2[6:16].replace('/', '-')
             date_1 = datetime.strptime(date1, '%Y-%m-%d')
             time_1 = datetime.timestamp(date_1)
             time_22 = datetime.strptime('2020/' + time[0:5], '%Y/%H:%M')
             time_2 = datetime.timestamp(time_22) - 1577826000.0
             time_3 = int(time_1) + int(time_2)
         except BaseException as err:
             continue
         if time_now - time_3 <= 86400:
             print(f'{"https://lenta.ru" + a2["href"]} {a2.text}')



elif header_number == 15:
    response = requests.get('https://lenta.ru/rubrics/realty/')

    second_parser = BeautifulSoup(response.text, features='html.parser')

    box = second_parser.select_one('div.b-yellow-box__wrap')
    contents = box.select('div.item')

    for content in contents:
        a2 = content.select_one('a')
        url2 = a2['href']
        text2 = a2.text
        print(f'{"https://lenta.ru" + url2} {text2[5:len(text2)]}')
else:
     print('Incorrect number of categories')
     exit(-1)
#print('a')