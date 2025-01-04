from telebot import *
from app.config import *
from app.scrap import *

bot = TeleBot(API_TOKEN)


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
                     reply_markup = menu_markup)

@bot.callback_query_handler(func=lambda call:True)
def handle_query(call):
    if call.data == 'search':
        bot.send_message(call.message.chat.id,"Please send the topic or keyboard you want to search for! 🎗🎫")
        bot.register_next_step_handler(call.message,search)
    elif call.data == 'help':
        bot.reply_to(call.message,"This bot allows you to search for academic publications metadata. Use the 'Search' button to begin")
    elif call.data == 'get':
        bot.send_message(call.message.chat.id,"Please send the topic or keyboard you want to find! 🎗🎫")
        bot.register_next_step_handler(call.message,find)
    elif call.data == 'download':
        bot.send_message(call.message.chat.id,"Please send the topic or keyboard you want to download! 🎗🎫")
        bot.register_next_step_handler(call.message, download)

def search(message):
    try:
        loading_msg = bot.reply_to(message, "Loading...... 💎💍")
        results = scrape(message.text)
        
        if not results:
            bot.edit_message_text("No results Found! 📞🎗", chat_id=loading_msg.chat.id, message_id=loading_msg.message_id)
        else:
            paper = results[0]  # Get the first result (or select another index if needed)
            paper_str = f"Title: {paper['Title']}\nAuthor: {paper['Author']}\nYear: {paper['Year']}\nCitations: {paper['Cite']}\nLink: {paper['Link']}\n"
            bot.send_message(message.chat.id, paper_str)
        
        bot.edit_message_text("Search Completed ✔✨!", chat_id=loading_msg.chat.id, message_id=loading_msg.message_id)
    
    except Exception as e:
        bot.edit_message_text(f"An Error Occurred! {e} ✖➰", chat_id=loading_msg.chat.id, message_id=loading_msg.message_id)



def find(message):
    ''
def download(message):
    ''

bot.polling()