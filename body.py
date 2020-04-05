import telebot

bot = telebot.TeleBot('1030330853:AAGe69afjFYwBl5XS5spjmScAFylIP1LOHk')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')





print('Started')
bot.polling()
