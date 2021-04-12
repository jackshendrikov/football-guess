import telebot
import sqlite3

from config import token
from football import gen_player
from leagues.pl_table import PL_TABLE
from random import choice


# new bot instance
bot = telebot.TeleBot(token)


# welcome menu
@bot.message_handler(commands=['start'])
def send_welcome(m):
    try:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row('⚽ Football', 'ℹ️ Help')
        user_markup.row('⚽ Start the game')

        db = sqlite3.connect("footballDB.sqlite")
        cursor = db.cursor()

        # Print SQLite version
        print("You are connected to - SQLite v", sqlite3.version, "\n")

        # Create Users Table
        cursor.execute('CREATE TABLE IF NOT EXISTS users (id SERIAL, userId VARCHAR NOT NULL);')
        db.commit()
        print("Table created successfully in SQLite! ")

        from_user = [m.from_user.id]
        cursor.execute('SELECT EXISTS(SELECT userId FROM users WHERE userId = ?)', from_user)
        check = cursor.fetchone()

        if not check[0]:
            cursor.execute('INSERT INTO users (userId) VALUES (?)', from_user)
            db.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into users table")
        else:
            count = cursor.rowcount
            print(count, "Record already exists")

        start_msg = 'Hey *{}* 👋, I\'m *FootGuessr Bot* 🤖!\n\n' \
                    'With my help you can play the game to guess 🤔 the player\'s name from their statistics.\n\n' \
                    'Also you can see:\n\t\t\t- results of football events ⚽' \
                    '\n\t\t\t- statistics of different leagues 📈' \
                    '\n\t\t\t- statistics of players 🏃🏽‍♀️\n\n' \
                    'Player data is taken from [Wiki](https://en.wikipedia.org/wiki/Main_Page).\n' \
                    'Football stats from [Livescores](livescores.com).\n\n' \
                    'Press any button below to interact with me 😀\n\n' \
                    'Made with ❤️ by *@jackshen* & *@rudek0*'

        bot.send_message(m.chat.id, start_msg.format(m.from_user.first_name), reply_markup=user_markup,
                         parse_mode="Markdown", disable_web_page_preview="True")

    except Exception as error:
        print("Error occurred", error)


# main menu
@bot.message_handler(regexp="👈 Main Menu")
def main_menu(m):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('⚽ Football', 'ℹ️ Help')
    user_markup.row('⚽ Start the game')

    user_msg = 'Return to the main menu.\n\n'
    bot.send_message(m.chat.id, user_msg, reply_markup=user_markup,
                     parse_mode="Markdown", disable_web_page_preview="True")


# help menu
@bot.message_handler(regexp="ℹ️ Help")
def command_help(m):
    help_text = "*FootGuessr Bot* 🤖: Send a private message to one of my creators *@jackshen*, *@rudek0* " \
                "if you need help with something."
    bot.send_message(m.chat.id, help_text, parse_mode='Markdown', disable_web_page_preview="True")


# football stat menu
@bot.message_handler(regexp="⚽ Football")
def send_football(m):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)

    user_markup.row('🏴󠁧󠁢󠁥󠁮󠁧󠁿󠁧󠁢󠁥󠁮󠁧󠁿 England', '🇪🇸 Spain')
    user_markup.row('🇩🇪 Germany', '🇫🇷 France')
    user_markup.row('🇮🇹 Italy', '🇺🇦 Ukraine')
    user_markup.row('👈 Main Menu')

    user_msg = 'Football Statistics from Top-Leagues 🔝 in Europe 🇪🇺\n\n'
    bot.send_message(m.chat.id, user_msg, reply_markup=user_markup,
                     parse_mode="Markdown", disable_web_page_preview="True")


# back to Main Football Menu
@bot.message_handler(regexp="👈 Back")
def football_back(m):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)

    user_markup.row('🏴󠁧󠁢󠁥󠁮󠁧󠁿󠁧󠁢󠁥󠁮󠁧󠁿 England', '🇪🇸 Spain')
    user_markup.row('🇩🇪 Germany', '🇫🇷 France')
    user_markup.row('🇮🇹 Italy', '🇺🇦 Ukraine')
    user_markup.row('👈 Main Menu')

    user_msg = 'Return to Main Football Menu.\n\n'
    bot.send_message(m.chat.id, user_msg, reply_markup=user_markup,
                     parse_mode="Markdown", disable_web_page_preview="True")


# English Premier League
@bot.message_handler(regexp="🏴󠁧󠁢󠁥󠁮󠁧󠁿󠁧󠁢󠁥󠁮󠁧󠁿 England")
def send_england(m):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('⚽ Premier League Table', '⚽ Premier League Scores')
    user_markup.row('⚽ Premier League Results (Last Week)', '👈 Back')

    user_msg = 'English Premier League Table and Scores.\n\n'
    bot.send_message(m.chat.id, user_msg, reply_markup=user_markup,
                     parse_mode="Markdown", disable_web_page_preview="True")


@bot.message_handler(regexp="⚽ Premier League Table")
def send_pl_table(message):
    user_msg = PL_TABLE
    bot.reply_to(message, user_msg)

@bot.message_handler(regexp='⚽ Start the game')
def guessing_game(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('⚽ Football', 'ℹ️ Help')
    user_markup.row('⚽ Start the game')

    reply = gen_player()
    text = "```" + str(reply[0]) + "```"
    bot.send_message(message.chat.id, text, reply_markup=user_markup, parse_mode="MarkdownV2")

    variants = [reply[1]]
    for i in range(3):
        flag = True
        while flag:
            temp = choice(list(open('players.txt', encoding='utf-8'))).replace('\n', '')
            random_player = " ".join(temp.split("_"))
            if random_player not in variants:
                variants.append(random_player)
                flag = False

    bot.send_poll(chat_id=message.chat.id, question="Try to guess the player, according to his career",
                  is_anonymous=True, options=variants, type="quiz",
                  correct_option_id=reply[1], reply_markup=user_markup,)

bot.polling()
