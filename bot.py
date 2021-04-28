import telebot
import sqlite3

from config import token
from random import choice, shuffle
from datetime import date

from football import gen_player
from leagues.league_table import ChampionshipTable
from leagues.league_scores import ChampionshipScores
from leagues.league_latest import ChampionshipLatest


# New Bot Instance
bot = telebot.TeleBot(token)
print("Bot is running")


# Welcome Menu
@bot.message_handler(commands=['start'])
def send_welcome(m):
    try:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row('⚽ Check Statistics', 'ℹ️ Help')
        user_markup.row('⚽ Start the Game')

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


# Main Menu
@bot.message_handler(regexp="👈 Main Menu")
def main_menu(m):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('⚽ Check Statistics', 'ℹ️ Help')
    user_markup.row('⚽ Start the Game')

    user_msg = 'Return to the main menu.\n\n'
    bot.send_message(m.chat.id, user_msg, reply_markup=user_markup,
                     parse_mode="Markdown", disable_web_page_preview="True")


# Help Menu
@bot.message_handler(regexp="ℹ️ Help")
def command_help(m):
    help_text = "*FootGuessr Bot* 🤖: Send a private message to one of my creators *@jackshen*, *@rudek0* " \
                "if you need help with something."
    bot.send_message(m.chat.id, help_text, parse_mode='Markdown', disable_web_page_preview="True")


# Football Stat Menu
@bot.message_handler(regexp="⚽ Check Statistics")
def send_football(m):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)

    user_markup.row('🏴󠁧󠁢󠁥󠁮󠁧󠁿󠁧󠁢󠁥󠁮󠁧󠁿 England', '🇪🇸 Spain')
    user_markup.row('🇩🇪 Germany', '🇫🇷 France')
    user_markup.row('🇮🇹 Italy', '🇺🇦 Ukraine')
    user_markup.row('👈 Main Menu')

    user_msg = 'Football Statistics from Top-Leagues 🔝 in Europe 🇪🇺\n\n'
    bot.send_message(m.chat.id, user_msg, reply_markup=user_markup,
                     parse_mode="Markdown", disable_web_page_preview="True")


# Back to Main Football Menu
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


# ============== English Premier League ==============
@bot.message_handler(regexp="🏴󠁧󠁢󠁥󠁮󠁧󠁿󠁧󠁢󠁥󠁮󠁧󠁿 England")
def send_england(m):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('⚽ Premier League Table', '⚽ Premier League Upcoming Events')
    user_markup.row('⚽ Premier League Latest Results', '👈 Back')

    user_msg = 'English Premier League Table and Scores.\n\n'
    bot.send_message(m.chat.id, user_msg, reply_markup=user_markup,
                     parse_mode="Markdown", disable_web_page_preview="True")


# Premier League Table
@bot.message_handler(regexp="⚽ Premier League Table")
def send_en_table(message):
    url = "http://www.livescores.com/soccer/england/premier-league/"
    user_msg = ChampionshipTable(url, table_width=9, table_height=21).create_table()
    bot.reply_to(message, user_msg, parse_mode="Markdown", disable_web_page_preview="True")


# Premier League Scores
@bot.message_handler(regexp="⚽ Premier League Upcoming Events")
def send_en_scores(message):
    url = "http://www.livescores.com/soccer/england/premier-league/"
    user_msg = ChampionshipScores(url).scrape_score()
    bot.reply_to(message, user_msg, parse_mode="Markdown", disable_web_page_preview="True")


# Premier League Results (Last Week)
@bot.message_handler(regexp="⚽ Premier League Latest Results")
def send_en_latest(message):
    url = "http://www.livescores.com/soccer/england/premier-league/results/7-days/"
    user_msg = ChampionshipLatest(url).parse_latest()
    bot.reply_to(message, user_msg, parse_mode="Markdown", disable_web_page_preview="True")


# ============== Spanish La Liga ==============
@bot.message_handler(regexp="🇪🇸 Spain")
def send_spain(m):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('⚽ La Liga Table', '⚽ La Liga Upcoming Events')
    user_markup.row('⚽ La Liga Latest Results', '👈 Back')

    user_msg = 'Spanish La Liga Table and Scores.\n\n'
    bot.send_message(m.chat.id, user_msg, reply_markup=user_markup,
                     parse_mode="Markdown", disable_web_page_preview="True")


# La Liga Table
@bot.message_handler(regexp="⚽ La Liga Table")
def send_es_table(message):
    url = "http://www.livescores.com/soccer/spain/primera-division/"
    user_msg = ChampionshipTable(url, table_width=9, table_height=21).create_table()
    bot.reply_to(message, user_msg, parse_mode="Markdown", disable_web_page_preview="True")


# La Liga Scores
@bot.message_handler(regexp="⚽ La Liga Upcoming Events")
def send_es_scores(message):
    url = "http://www.livescores.com/soccer/spain/primera-division/"
    user_msg = ChampionshipScores(url).scrape_score()
    bot.reply_to(message, user_msg, parse_mode="Markdown", disable_web_page_preview="True")


# La Liga Results (Last Week)
@bot.message_handler(regexp="⚽ La Liga Latest Results")
def send_es_latest(message):
    url = "http://www.livescores.com/soccer/spain/primera-division/results/7-days/"
    user_msg = ChampionshipLatest(url).parse_latest()
    bot.reply_to(message, user_msg, parse_mode="Markdown", disable_web_page_preview="True")


# ============== German Bundesliga ==============
@bot.message_handler(regexp="🇩🇪 Germany")
def send_germany(m):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('⚽ Bundesliga Table', '⚽ Bundesliga Upcoming Events')
    user_markup.row('⚽ Bundesliga Latest Results', '👈 Back')

    user_msg = 'German Bundesliga Table and Scores.\n\n'
    bot.send_message(m.chat.id, user_msg, reply_markup=user_markup,
                     parse_mode="Markdown", disable_web_page_preview="True")


# Bundesliga Table
@bot.message_handler(regexp="⚽ Bundesliga Table")
def send_de_table(message):
    url = "http://www.livescores.com/soccer/germany/bundesliga/"
    user_msg = ChampionshipTable(url, table_width=9, table_height=19).create_table()
    bot.reply_to(message, user_msg, parse_mode="Markdown", disable_web_page_preview="True")


# Bundesliga Scores
@bot.message_handler(regexp="⚽ Bundesliga Upcoming Events")
def send_de_scores(message):
    url = "http://www.livescores.com/soccer/germany/bundesliga/"
    user_msg = ChampionshipScores(url).scrape_score()
    bot.reply_to(message, user_msg, parse_mode="Markdown", disable_web_page_preview="True")


# Bundesliga Results (Last Week)
@bot.message_handler(regexp="⚽ Bundesliga Latest Results")
def send_de_latest(message):
    url = "http://www.livescores.com/soccer/germany/bundesliga/results/7-days/"
    user_msg = ChampionshipLatest(url).parse_latest()
    bot.reply_to(message, user_msg, parse_mode="Markdown", disable_web_page_preview="True")


# ============== French Ligue 1 ==============
@bot.message_handler(regexp="🇫🇷 France")
def send_france(m):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('⚽ Ligue 1 Table', '⚽ Ligue 1 Upcoming Events')
    user_markup.row('⚽ Ligue 1 Latest Results', '👈 Back')

    user_msg = 'French Ligue 1 Table and Scores.\n\n'
    bot.send_message(m.chat.id, user_msg, reply_markup=user_markup,
                     parse_mode="Markdown", disable_web_page_preview="True")


# Ligue 1 Table
@bot.message_handler(regexp="⚽ Ligue 1 Table")
def send_fr_table(message):
    url = "http://www.livescores.com/soccer/france/ligue-1/"
    user_msg = ChampionshipTable(url, table_width=9, table_height=21).create_table()
    bot.reply_to(message, user_msg, parse_mode="Markdown", disable_web_page_preview="True")


# Ligue 1 Scores
@bot.message_handler(regexp="⚽ Ligue 1 Upcoming Events")
def send_fr_scores(message):
    url = "http://www.livescores.com/soccer/france/ligue-1/"
    user_msg = ChampionshipScores(url).scrape_score()
    bot.reply_to(message, user_msg, parse_mode="Markdown", disable_web_page_preview="True")


# Ligue 1 Results (Last Week)
@bot.message_handler(regexp="⚽ Ligue 1 Latest Results")
def send_fr_latest(message):
    url = "http://www.livescores.com/soccer/france/ligue-1/results/7-days/"
    user_msg = ChampionshipLatest(url).parse_latest()
    bot.reply_to(message, user_msg, parse_mode="Markdown", disable_web_page_preview="True")


# ============== Italian Serie A ==============
@bot.message_handler(regexp="🇮🇹 Italy")
def send_italy(m):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('⚽ Serie A Table', '⚽ Serie A Upcoming Events')
    user_markup.row('⚽ Serie A Latest Results', '👈 Back')

    user_msg = 'Italian Serie A Table and Scores.\n\n'
    bot.send_message(m.chat.id, user_msg, reply_markup=user_markup,
                     parse_mode="Markdown", disable_web_page_preview="True")


# Serie A Table
@bot.message_handler(regexp="⚽ Serie A Table")
def send_it_table(message):
    url = "http://www.livescores.com/soccer/italy/serie-a/"
    user_msg = ChampionshipTable(url, table_width=9, table_height=21).create_table()
    bot.reply_to(message, user_msg, parse_mode="Markdown", disable_web_page_preview="True")


# Serie A Scores
@bot.message_handler(regexp="⚽ Serie A Upcoming Events")
def send_it_scores(message):
    url = "http://www.livescores.com/soccer/italy/serie-a/"
    user_msg = ChampionshipScores(url).scrape_score()
    bot.reply_to(message, user_msg, parse_mode="Markdown", disable_web_page_preview="True")


# Serie A Results (Last Week)
@bot.message_handler(regexp="⚽ Serie A Latest Results")
def send_it_latest(message):
    url = "http://www.livescores.com/soccer/italy/serie-a/results/7-days/"
    user_msg = ChampionshipLatest(url).parse_latest()
    bot.reply_to(message, user_msg, parse_mode="Markdown", disable_web_page_preview="True")


# ============== Ukrainian Premier League ==============
@bot.message_handler(regexp="🇺🇦 Ukraine")
def send_ukraine(m):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('⚽ UPL Table', '⚽ UPL Upcoming Events')
    user_markup.row('⚽ UPL Latest Results', '👈 Back')

    user_msg = 'Ukrainian Premier League Table and Scores.\n\n'
    bot.send_message(m.chat.id, user_msg, reply_markup=user_markup,
                     parse_mode="Markdown", disable_web_page_preview="True")


# UPL Table
@bot.message_handler(regexp="⚽ UPL Table")
def send_ua_table(message):
    url = "https://www.livescores.com/soccer/ukraine/premier-league/"
    user_msg = ChampionshipTable(url, table_width=9, table_height=15).create_table()
    bot.reply_to(message, user_msg, parse_mode="Markdown", disable_web_page_preview="True")


# UPL Scores
@bot.message_handler(regexp="⚽ UPL Upcoming Events")
def send_ua_scores(message):
    url = "https://www.livescores.com/soccer/ukraine/premier-league/"
    user_msg = ChampionshipScores(url).scrape_score()
    bot.reply_to(message, user_msg, parse_mode="Markdown", disable_web_page_preview="True")


# UPL Results (Last Week)
@bot.message_handler(regexp="⚽ UPL Latest Results")
def send_ua_latest(message):
    url = "http://www.livescores.com/soccer/ukraine/premier-league/results/7-days/"
    user_msg = ChampionshipLatest(url).parse_latest()
    bot.reply_to(message, user_msg, parse_mode="Markdown", disable_web_page_preview="True")


# Football Game Type
@bot.message_handler(regexp="⚽ Start the Game")
def send_football(m):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)

    user_markup.row('Guessing by the picture', 'Guessing by the career')

    user_msg = 'Choose the type of the game'
    bot.send_message(m.chat.id, user_msg, reply_markup=user_markup,
                     parse_mode="Markdown", disable_web_page_preview="True")

# ============== Guess Player by his/her Statistics (Poll) ==============
@bot.message_handler(regexp='Guessing by the career')
def guessing_game(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('⚽ Check Statistics', 'ℹ️ Help')
    user_markup.row('Guessing by the picture', "Guessing by the career")

    reply = gen_player()
    text = "```" + str(reply[0]) + "```"
    bot.send_message(message.chat.id, text, reply_markup=user_markup, parse_mode="MarkdownV2")

    correct_answer = reply[1]
    variants = [reply[1]]
    for i in range(3):
        flag = True
        while flag:
            temp = choice(list(open('players.txt', encoding='utf-8'))).replace('\n', '')
            random_player = " ".join(temp.split("_"))
            if random_player not in variants:
                variants.append(random_player)
                flag = False
    shuffle(variants)

    bot.send_poll(chat_id=message.chat.id, question="Try to guess the player, according to his career",
                  is_anonymous=True, options=variants, type="quiz",
                  correct_option_id=variants.index(correct_answer), reply_markup=user_markup,)

# ============== Guess Player by his/her picture ==============
@bot.message_handler(regexp='Guessing by the picture')
def guessing_game(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('⚽ Check Statistics', 'ℹ️ Help')
    user_markup.row('Guessing by the picture', "Guessing by the career")

    reply = gen_player()

    correct_answer = reply[1]
    variants = [reply[1]]
    for i in range(3):
        flag = True
        while flag:
            temp = choice(list(open('players.txt', encoding='utf-8'))).replace('\n', '')
            random_player = " ".join(temp.split("_"))
            if random_player not in variants:
                variants.append(random_player)
                flag = False
    shuffle(variants)

    bot.send_photo(message.chat.id, reply[2])

    bot.send_poll(chat_id=message.chat.id, question="Try to guess the player, according to his career",
                  is_anonymous=True, options=variants, type="quiz",
                  correct_option_id=variants.index(correct_answer), reply_markup=user_markup,)

bot.polling()



