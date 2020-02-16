import requests
from bs4 import BeautifulSoup

response = requests.get('https://habr.com/ru/')

main_parser = BeautifulSoup(response.text, features="html.parser")

navbar_links = main_parser.select_one('ul#navbar-links.nav-links')
categories = navbar_links.select('li.nav-links__item')

for i in range(len(categories)):
    category = categories[i]
    text = category.text.replace('\n', '')
    print(f'{i + 1}] {text}')

print('Select number of categories: ', end='')
numberOfCategory = int(input())

if numberOfCategory - 1 < 0 or numberOfCategory - 1 >= len(categories):
    print('Incorrect number of category')
    exit(-1)

category = categories[numberOfCategory - 1]
print(category.text)
# print(category)
a = category.select_one('a')
# print(a)
url = a.attrs['href']
response = requests.get(url)
second_parser = BeautifulSoup(response.text, features= 'html.parser')
posts_parser = second_parser.select_one('div.posts_list')
posts = posts_parser.select('li.content-list__item.content-list__item_post.shortcuts_item')
for post in posts:
    try:
        h2 = post.select_one('h2.post__title')
        a2 = h2.select_one('a')
        url2 = a2.attrs['href']
        url2_name = a2.text
        print(url2_name, url2)
    except BaseException as err:
        continue
#print(second_parser)
