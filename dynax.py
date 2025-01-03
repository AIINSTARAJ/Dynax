from telebot import *
from app.config import *
from app.scrap import *

bot = TeleBot(API_TOKEN)

def menu():
    menu_markup = util.quick_markup({
        'Search':{
            'callback_data':'search',
        },
        'GET':{
            'callback_data':'get',
        },
        'HELP':{
            'callback_data':'help',
        },
        'DOWNLOAD':{
            'callback_data':'download',
        },
    },row_width=2)
    return menu_markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,START_MSG)

@bot.message_handler(commands=['about'])
def start(message):
    bot.reply_to(message,ABOUT_MSG)

@bot.message_handler(commands=['menu'])
def menu(message):
    bot.send_message(message.chat.id,
                     "Interface with Dynax! 💍💎",
                     reply_markup = menu())

@bot.callback_query_handler(func=lambda call:True)
def handle_query(call):
    if call.data == 'search':
        bot.send_message(call.message.chat.id,"Please send the topic or keyboard you want to search for! 🎗🎫")
        bot.register_next_step_handler(call.message,search)
    elif call.data == 'help':
        bot.send_message(call.message.chat.id,"This bot allows you to search for academic publications metadata. Use the 'Search' button to begin")
    elif call.data == 'get':
        bot.send_message(call.message.chat.id,"Please send the topic or keyboard you want to find! 🎗🎫")
        bot.register_next_step_handler(call.message,find)
    elif call.data == 'download':
        bot.send_message(call.message.chat.id,"Please send the topic or keyboard you want to download! 🎗🎫")
        bot.register_next_step_handler(call.message,download)

def search(message):
    try:
        loading_msg = bot.reply_to(message,"Loading...... 💎💍")
        results = scrape(message)
        if not results:
            bot.edit_message_text("No results Found! 📞🎗",chat_id=loading_msg.chat.id,message_id=loading_msg.message_id)
        for i,paper in enumerate(results):
            bot.send_message(message.chat.id, f"{i + 1}.\n Title : {paper['Title']}\n Author: {paper['Author']}\n Year: {paper['Year']}\n Citations: {paper['Cited']}\n Link: {paper['Link']}\n")
            time.sleep(0.5)
        bot.edit_message_text("Search Completed ✔✨!",chat_id=loading_msg.chat.id,message_id=loading_msg.message_id)
    except Exception as E:
        bot.edit_message_text("An Error Occured! ✖➰",chat_id=loading_msg.chat.id,message_id=loading_msg.message_id)


def find(message):
    ''
def download(message):
    ''

bot.polling()