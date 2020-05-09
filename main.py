import requests
from bs4 import BeautifulSoup
from _datetime import datetime


def habr(start_number):
    response = requests.get('https://habr.com/ru/')

    now_sites = []

    main_parser = BeautifulSoup(response.text, features="html.parser")

    navbar_links = main_parser.select_one('ul#navbar-links.nav-links')
    categories = navbar_links.select('li.nav-links__item')

    time_now = datetime.time(datetime.now())
    s_time_now = time_now.hour * 3600 + time_now.minute * 60 + time_now.second + 86400

    for i in range(len(categories)):
        category = categories[i]
        text = category.text.replace('\n', '')

    numberOfCategory = start_number

    category = categories[numberOfCategory - 1]
    a = category.select_one('a')
    url = a.attrs['href']
    response = requests.get(url)
    second_parser = BeautifulSoup(response.text, features='html.parser')
    posts_parser = second_parser.select_one('div.posts_list')
    posts = posts_parser.select('li.content-list__item.content-list__item_post.shortcuts_item')
    for post in posts:
        try:
            articles = post.select_one('article.post_preview')
            header = articles.select_one('header.post__meta')
            time = header.select_one('span.post__time').text
            h2 = post.select_one('h2.post__title')
            t = time[:7]
            a2 = h2.select_one('a')
            url2 = a2.attrs['href']
            url2_name = a2.text
            if (t == 'сегодня'):
                sites_of_category = f'{url2} {url2_name}'
                now_sites.append(sites_of_category)
            elif time[:5] == 'вчера':
                post_time = int(time[8:10]) * 3600 + int(time[12:13]) * 60
                if s_time_now - post_time <= 86400:
                    sites_of_category = f'{url2} {url2_name}'
                    now_sites.append(sites_of_category)
        except BaseException as err:
            continue
    return now_sites
