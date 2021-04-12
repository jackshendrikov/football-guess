import telebot


from config import token
from football import gen_player



bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "To start the game, send +")

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == '+':
        bot.send_message(message.chat.id, 'Try to guess the player, according to his career')
        text = "```"+str(gen_player())+"```"
        bot.send_message(message.chat.id, text, parse_mode="MarkdownV2")


bot.polling()


