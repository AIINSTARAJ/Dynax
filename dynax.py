from telebot import *
from app.config import *
from app.scrap import *

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


def read_():
    with open('readme.md',encoding='cp1252') as r:
        content_ = r.read()
        return content_
    

def split_message(text, max_length=4000):
    lines = text.splitlines()
    chunks, current_chunk = [], []
    current_length = 0
    for line in lines:
        if current_length + len(line) + 1 > max_length:
            chunks.append('\n'.join(current_chunk))
            current_chunk = [line]
            current_length = len(line) + 1
        else:
            current_chunk.append(line)
            current_length += len(line) + 1
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
    return chunks

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,START_MSG)

@bot.message_handler(commands=['about'])
def start(message):
    bot.send_message(message.chat.id,ABOUT_MSG)

@bot.message_handler(commands=['info'])
def res_(message):
    con = read_()
    long_text = con.replace('_', '').replace('*', '').replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('~', '').replace('`', '').replace('>', '').replace('#', '').replace('+', '').replace('-', '').replace('=', '').replace('|', '').replace('{', '').replace('}', '').replace('.', '').replace('!', '')
    chunks = split_message(long_text)
    for chunk in chunks:
        bot.send_message(message.chat.id, text=chunk, parse_mode="MarkdownV2")


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
        paper_str = f"<b>Title:</b> {paper['Title']}\n<b>Author: {paper['Author']}</b>\n<b>Year:</b> {paper['Year']}\n<b>Citations:</b> {paper['Cite']}\n<b>Link:</b> <a href='{paper['Link']}'>{paper['Link']}</a>"
        bot.send_message(message.chat.id, paper_str,parse_mode="HTML", disable_web_page_preview=False)
        time.sleep(0.1)
        send_results_separately(results, index + 1, message)

def search(message):
    try:
        loading_msg = bot.reply_to(message, "Loading...... 💎💍")
        results = scrape(message.text) 
        if not results:
            bot.edit_message_text("No results Found! 📞🎗", chat_id=loading_msg.chat.id, message_id=loading_msg.message_id)
        else:
            send_results_separately(results, message=message)       
        bot.edit_message_text(f"Search Completed! : <b>{message.text}</b> ✔✨", parse_mode='HTML',chat_id=loading_msg.chat.id, message_id=loading_msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"An Error Occurred! {e} ✖➰", chat_id=loading_msg.chat.id, message_id=loading_msg.message_id)

bot.polling()