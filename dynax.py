from telebot import *
from app.config import *
from app.logic.scrap import *

bot = TeleBot(API_TOKEN)



menu_markup = util.quick_markup({
        'Search':{
            'callback_data':'search',
        },
        'HELP':{
            'callback_data':'help',
        },
    },
    row_width=2
)


def read_(file):
    with open(file,encoding='cp1252') as r:
        content_ = r.read()
        return content_

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,START_MSG)

@bot.message_handler(commands=['about'])
def start(message):
    bot.send_message(message.chat.id,ABOUT_MSG)


@bot.message_handler(commands=['menu'])
def menu(message):
    bot.send_message(message.chat.id,
                     "Interface with Dynax! 💍💎",
                     reply_markup = menu_markup)

@bot.callback_query_handler(func=lambda call:True)
def handle_query(call):
    bot.edit_message_text(f"Command: <b>'{call.data.upper()}'</b>", parse_mode="HTML", chat_id=call.message.chat.id, message_id=call.message.message_id)
    if call.data == 'search':
        bot.send_message(call.message.chat.id,"Please enter the topic or keyword you want to search for! 🎗🎫")
        bot.register_next_step_handler(call.message,search)
    elif call.data == 'help':
        bot.reply_to(call.message,"This bot allows you to search for academic publications metadata. Use the 'Search' button to begin")

def send_results_separately(results, index=0, message=None):
    if index < len(results):
        paper = results[index]
        paper_str = f"<b>Title:</b> {paper['title']}\n<b>Author: {paper['authors']}</b>\n<b>Year:</b> {paper['year']}\n<b>Citations:</b> {paper['citations']}\n<b>Link:</b> <a href='{paper['url']}'>{paper['url']}</a>"
        bot.send_message(message.chat.id, paper_str,parse_mode="HTML", disable_web_page_preview=False)
        time.sleep(0.1)
        send_results_separately(results, index + 1, message)

def search(message):
    try:
        loading_msg = bot.reply_to(message, "Loading...... 💎💍")
        results =search(message.text) 
        if not results:
            bot.edit_message_text("No results Found! 📞🎗", chat_id=loading_msg.chat.id, message_id=loading_msg.message_id)
        else:
            send_results_separately(results, message=message)       
        bot.edit_message_text(f"Search Completed! : <b>{message.text}</b> ✔✨", parse_mode='HTML',chat_id=loading_msg.chat.id, message_id=loading_msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"An Error Occurred! {e} ✖➰", chat_id=loading_msg.chat.id, message_id=loading_msg.message_id)

bot.polling()