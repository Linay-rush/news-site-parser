import time
import telebot
import schedule
from lentaAction import lenta
from Users import Users
from main import habr
from meduza_v2 import meduza


bot = telebot.TeleBot('1030330853:AAGe69afjFYwBl5XS5spjmScAFylIP1LOHk')
key_board_start = telebot.types.ReplyKeyboardMarkup(True, True)
key_board_start.row('/start')

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

time_at = '20:00'
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
    if not user:
        bot.send_message(message.chat.id, 'Напиши мне /start', reply_markup=key_board_start)
    elif user.state == 1:

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

        else:
            bot.send_message(message.chat.id, 'Ты мне что отправил, шалопай, шельмец??? Выбирай из предложенных '
                                              'вариантов', reply_markup=key_board1)

    elif user.state == 2:
        categories = sites[user.site]

        if text in categories:
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
        elif text == 'Выход':
            user.state = 1
            bot.send_message(message.chat.id, 'Выбери сайт(ы), на который(ые) ты хочешь подписаться',
                             reply_markup=key_board1)
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


def cron_action():
    for site in sites:
        categories = sites[site]

        for i in range(len(categories)):
            category = categories[i]

            news = ''
            if site == 'lenta.ru':
                news = lenta(i + 1)
            elif site == 'habr.com':
                news = habr(i)
            elif site == 'meduza.io':
                news = meduza(i + 1)

            for id in users:
                user = users[id]
                user_categories = user.sites.get(site)

                if user_categories is None:
                    continue

                if category in user_categories != -1:
                    bot.send_message(id, f'{site}: {category}')
                    for i in range(len(news)):
                        bot.send_message(id, news[i])


def process_action():
    while 1:
        schedule.run_pending()
        time.sleep(1)


from threading import Thread

if __name__ == "__main__":
    schedule.every.day.at(time_at).do(cron_action)

    Thread(target=process_action).start()

    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
            time.sleep(15)
