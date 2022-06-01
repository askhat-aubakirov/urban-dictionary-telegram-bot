'''
May 30th, 2022

This bot gets the message from user and looks for a definition 
and usage examples from Urban Dictionary.
                                                This is pure fun)

Big thanks to Daniel Maltese for sharing the brilliant tutorial on web scraper telegram bot!
Tutorial is located here: https://www.danielemaltese.com/posts/web-scarper-telegram-bot-python/

Hope this can be helpful!

by Askhat Aubakirov
e-mail: askhat.aubakirov@yahoo.com
LinkedIn: https://www.linkedin.com/in/askhattio/
'''

#importing all of the necessary libraries
from bs4 import BeautifulSoup
import requests
from telegram import Update, constants
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    Filters,
)
from emoji import emojize #for showing some emojis
import random #to randomly choose some emojis

#giving token to the program to interact with API
updater = Updater("TOKEN")

#set of some emojis picked for this project
my_emojis = [":thumbs_up:", ":cat_face:", ":star:", ":smiling_face_with_sunglasses:", ":confused_face:"]

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f"Hello, {update.effective_user.first_name}\nI look for meanings of words from Urban Dictionary {emojize(random.choice(my_emojis))} \n(For more info try /help)")
    update.message.reply_text("Just give me the word! " + emojize(":smiling_face_with_sunglasses:"))

def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("<b>Usage</b>: This bot is able to accept words and look for a definition of them on Urban Dictionary.\n\nIf you want to receive some info on developer, type /dev\nremember you can start all over using /start \nYou can have this help message shown again by using /help \n\nHave fun!", parse_mode=telegram.constants.PARSEMODE_HTML)

def dev(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(emojize(":smiling_face_with_sunglasses:") + "Developed by Askhat Aubakirov, \ne-mail: askhat.aubakirov@yahoo.com \nMy LinkedIn: https://www.linkedin.com/in/askhattio/")

def get_word(update: Update, context: CallbackContext) -> None:

    try:
        #creating url out of the base url + the word user types to the bot
        url = "https://www.urbandictionary.com/define.php?term=" + update.message.text.lower().strip()
        #performing request to the url created
        page = requests.get(url)
        #force the encoding manually to UTF-8 so as to prevent corrupted decoding -> 
        # -> otherwise it leads to incorrect display of emojis and cyrillic letters
        page.encoding = "utf-8"
        #retrieving webpage contents with BeautifulSoup
        soup = BeautifulSoup(page.text, "html.parser") 

        #looking for and retrieving the text data with definition and examples from the page
        definiton = soup.find("div", {"class": "meaning mb-4"}).text
        examples = soup.find("div", {"class": "example italic mb-4"}).text

        #sending messages to user with the scraped definitions and examples
        update.message.reply_text(f"<b>Here is the <i>definition</i> of {update.message.text}:</b> \n{definiton} \n" + emojize(random.choice(my_emojis)), parse_mode=constants.PARSEMODE_HTML)
        update.message.reply_text(f"<b>Here are the <i>examples</i> of usage:</b> \n{examples} \n" + emojize(random.choice(my_emojis)), parse_mode=constants.PARSEMODE_HTML)
    
    except:
        #if the routine code doesn't work, bot will ask user for another word(s) 
        update.message.reply_text(emojize("Something went wrong :confused_face: \nProbably, thing you have just written is not represented in the Urban Dictionary database \nTry some other word"))

#in case of undefined commands:
def unknown(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f"Sorry, {update.effective_user.first_name}. \nI don't understand the command " + emojize(":confused_face:"))
    update.message.reply_text("Check the command, please")

#adding hanlders to constantly "look for" appropriate commands and words
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("help", help))
updater.dispatcher.add_handler(CommandHandler("dev", dev))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.text, get_word))

#starting the bot and making it listen
updater.start_polling()
updater.idle()
