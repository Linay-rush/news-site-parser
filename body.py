import telebot
import schedule
def lenta(start_number):
    import requests
    from bs4 import BeautifulSoup
    from datetime import datetime

    response = requests.get('https://lenta.ru')
    now_sites = []
    time_now = datetime.timestamp(datetime.today())

    main_parser = BeautifulSoup(response.text, features='html.parser')
    sidebar_menu = main_parser.select_one('ul.b-sidebar-menu__list')
    headers = sidebar_menu.select('li.b-sidebar-menu__list-item')
    for i in range(len(headers) - 1):
        header = headers[i]
        text = header.text
    header_number = start_number

    if 0 <= header_number - 1 < len(headers) - 1:
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
                sites_of_category = f'{"https://lenta.ru" + a2["href"]} {a2.text}'
                now_sites.append(sites_of_category)
        return now_sites



    elif header_number == 15:
        response = requests.get('https://lenta.ru/rubrics/realty/')

        second_parser = BeautifulSoup(response.text, features='html.parser')

        box = second_parser.select_one('div.b-yellow-box__wrap')
        contents = box.select('div.item')

        for content in contents:
            a2 = content.select_one('a')
            url2 = a2['href']
            text2 = a2.text
            sites_of_category = f'{"https://lenta.ru" + url2} {text2[5:len(text2)]}'
            now_sites.append(sites_of_category)
        return now_sites
    else:
        print('Incorrect number of categories')
        exit(-1)


bot = telebot.TeleBot('1030330853:AAGe69afjFYwBl5XS5spjmScAFylIP1LOHk')

key_board1 = telebot.types.ReplyKeyboardMarkup(True, True)
key_board1.row('lenta.ru', 'habr.com', 'meduza.io', 'Выход')

key_board_lenta = telebot.types.ReplyKeyboardMarkup(True)
key_board_lenta.row('Выход', 'Главное', 'Россия', 'Мир')
key_board_lenta.row('Бывший СССР', 'Экономика', 'Силовые структуры')
key_board_lenta.row('Наука и техника', 'Культура', 'Спорт')
key_board_lenta.row('Инттернет и СМИ', 'Ценности', 'Путешествия')
key_board_lenta.row('Из жизни', 'Дом', 'Последние новости')

key_board_habr = telebot.types.ReplyKeyboardMarkup(True)
key_board_habr.row('Выход', 'Все потоки', 'Разработка', 'Научпоп')
key_board_habr.row('Администрирование', 'Дизайн', 'Менеджмент', 'Маркетинг')

key_board_meduza = telebot.types.ReplyKeyboardMarkup(True)
key_board_meduza.row('Выход', 'Новости', 'Истории', 'Разбор')
key_board_meduza.row('Игры', 'Шапито', 'Подкасты', 'Кононавирус')

class Users:
    def __init__(self, id):
        self.id = id
        self.sites = dict()
        self.state = 0
        self.site = ''


users = dict()
sites = dict()
sites['lenta.ru'] = ['Главное', 'Россия', 'Мир', 'Бывший СССР', 'Экономика', 'Силовые структуры', 'Наука и техника',
                     'Культура', 'Спорт', 'Интернет и СМИ', 'Ценности', 'Путешествия', 'Из жизни', 'Дом',
                     'Последние новости']
sites['habr.com'] = ['Все потоки', 'Разработка', 'Научпоп', 'Администрирование', 'Дизайн', 'Менеджмент',
                    'Маркетинг']
sites['meduza.io'] = ['Новости', 'Истории', 'Разбор', 'Игры', 'Шапито', 'Подкасты', 'Коронавирус']

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')

    user = users.get(message.chat.id)
    if not user:
        user = Users(message.chat.id)
        users[message.chat.id] = user

    bot.send_message(message.chat.id, 'Выбери сайт(ы), на который(ые) ты хочешь подписаться', reply_markup=key_board1)
    user.state = 1

@bot.message_handler(content_types=["text"])
def site_handler(message):
    user = users.get(message.chat.id)
    text = message.text
    if user.state == 1:

        if text == 'lenta.ru':
            user.site = text
            bot.send_message(message.chat.id, 'Выбери категорию(ии), на которую(ые) ты хочешь подписаться',
                             reply_markup=key_board_lenta)
            user.state += 1

        elif text == 'habr.com':
            user.site = text
            bot.send_message(message.chat.id, 'Выбери категорию(ии), на которую(ые) ты хочешь подписаться',
                             reply_markup=key_board_habr)
            user.state += 1

        elif text == 'meduza.io':
            user.site = text
            bot.send_message(message.chat.id, 'Выбери категорию(ии), на которую(ые) ты хочешь подписаться',
                             reply_markup=key_board_meduza)
            user.state += 1

        elif text == 'Выход':
            user.state = 0

        else: bot.send_message(message.chat.id, 'Ты мне что отправил, шалопай, шельмец??? Выбирай из предложенных '
                                                'вариантов', reply_markup=key_board1)

    elif user.state == 2:
        categories = sites[user.site]

        if text == 'Выход':
            user.state = 1
            bot.send_message(message.chat.id, 'Выбери сайт(ы), на который(ые) ты хочешь подписаться',
                             reply_markup=key_board1)

        elif categories.index(text) != -1:
            user_site_categories = user.sites.get(user.site)
            if not user_site_categories:
                user_site_categories = [text]
                user.sites[user.site] = user_site_categories
            else:
                user_site_categories.append(text)
            if user.site == 'lenta.ru':
                bot.send_message(message.chat.id, 'Выбери категорию(ии), на которую(ые) ты хочешь подписаться',
                                 reply_markup=key_board_lenta)

            elif user.site == 'habr.com':
                bot.send_message(message.chat.id, 'Выбери категорию(ии), на которую(ые) ты хочешь подписаться',
                                 reply_markup=key_board_habr)

            elif user.site == 'meduza.io':
                bot.send_message(message.chat.id, 'Выбери категорию(ии), на которую(ые) ты хочешь подписаться',
                                 reply_markup=key_board_meduza)
        else:
            bot.send_message(message.chat.id, 'Ты мне что отправил, шалопай, шельмец??? Выбирай из предложенных '
                                              'вариантов')

            if user.site == 'lenta.ru':
                bot.send_message(message.chat.id, 'Выбери категорию(ии), на которую(ые) ты хочешь подписаться',
                           reply_markup=key_board_lenta)

            elif user.site == 'habr.com':
                bot.send_message(message.chat.id, 'Выбери категорию(ии), на которую(ые) ты хочешь подписаться',
                           reply_markup=key_board_habr)

            elif user.site == 'meduza.io':
                bot.send_message(message.chat.id, 'Выбери категорию(ии), на которую(ые) ты хочешь подписаться',
                           reply_markup=key_board_meduza)
for i in range (15):
    schedule.every().day.at('16:00').do(lenta, i+1)
    print(now_sites)
bot.polling(none_stop=True)
