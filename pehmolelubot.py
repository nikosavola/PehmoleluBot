# -*- coding: utf-8 -*-
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import os
import logging, random, time

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s'
)
fh = logging.FileHandler('spam.log') #filehandler
fh.setLevel(logging.INFO)


token = os.environ['TG_TOKEN']

########  globaalit  init ###
catIsHungry = False
dogIsHungry = False
catFed = 0
fedTime = time.clock()
mybots = {} # kaikki nykyiset chatit

def start(update, context):
    mybots[update.message.chat_id] = bot
    update.message.reply_text('Heissulivei! Tämä on PehmoleluBotti,  jolla voi esim. ruokkia kisulia.')


def hello_world(bot, update):
	print(update)
	chat_id = update.message.chat.id
	bot.sendMessage(chat_id, 'Hello world!')


def dog_hungry(bot, update):
    #print(update) # log that shite
    chat_id = update.message.chat.id
    global dogIsHungry
    if dogIsHungry:
        teksti = "dog on nälkäinen! *murr*"
    else:
        teksti = "doglla ei ole näläkä!"
    bot.sendSticker(chat_id, sticker_map.get('dog'))
    bot.sendMessage(chat_id, teksti)
    dogIsHungry = False


def cat_hungry(bot, update):
    print(update) # log that shite
    chat_id = update.message.chat.id
    global catIsHungry
    if catIsHungry:
        tekstiCat = "Kisuli on nälkäinen! *miaaaaau*"
    else:
        tekstiCat = "Kummasti kisuli ei ole nälkäinen!"
    #catIsHungry = False
    bot.sendSticker(chat_id, sticker_map.get('kisuli'))
    bot.sendMessage(chat_id, tekstiCat)


def cat_hungry_random():
    return random.randint(10800, 28800) # 3h<t<8h

def eaten_recently():
    global fedTime
    if fedTime - time.clock() > -(3*60*60):    # jos kulunut alle 3h
        return True
    else:
        return False

#       EI TÄLLÄ HETKELLÄ OTA MIHINKÄÄN CHATTIIN, LAITA KAIKKIIN RYHMIIN MIHIN LISÄTTY
def cat_gets_hungry(a,b):
    global catIsHungry
    catIsHungry = True
    return

def feed_cat(bot, update):
    print(update) # log that shite
    chat_id = update.message.chat.id
    global catIsHungry, catFed, fedTime
    fedTime = time.clock()
    catIsHungry = False
    catFed += 1
    bot.sendSticker(chat_id, sticker_map.get('kisuli'))
    bot.sendMessage(chat_id, 'Kisuli syö namun. Ei ole nyt ainakaan nälkäinen!')


def cat_fed_times(bot, update):
    chat_id = update.message.chat.id
    global catFed
    fedTeksti = 'Kisulille on annettu namuja ' + str(catFed) + ' =^._.^='
    bot.sendMessage(chat_id, fedTeksti)

def handle_message(bot, update):
    """ Handles messages that match "all" filter """
    chat_id = update.message.chat.id

    # Check that we are dealing with message involving text
    if update.message.text:
        words = update.message.text.split()
        global catIsHungry

        if 'keksi' in words or 'Keksi' in words: # tee tämä hienommaksi
            catIsHungry = True
            ran = ['Kisuli kuulee sanan \'keksi\', hän on nyt nälkäinen.',
                    'Kisuli tuli nälkäiseksi kuullessaan sanan \'keksi\'']
            random.shuffle(ran)
            bot.sendMessage(chat_id, ran[0])

        elif not eaten_recently() and catIsHungry:
            bot.sendSticker(chat_id, sticker_map.get('kisuli'))
            ran = ['Kisuli ei ole syönyt johonkin aikaan, kisulilla on nälkä!',
                    'Kisuli on nälkäinen. *murrr*',
                    'Kisuli tahtoo ruokaa  /ᐠ｡‸｡ᐟ\\']
            random.shuffle(ran)
            bot.sendMessage(chat_id, ran[0] )
        # Loop through keywords and stickers in pairs
        for hotword, sticker in sticker_map.items():

            # Send a sticker for each matching keyword
            if hotword in words:
                bot.sendSticker(chat_id, sticker)

sticker_map = {
    'dog': 'CAADBAADHQADlS56CMNshytcGo3hAg',
    'winston': 'CAADBAADIQADlS56CKuKJ27vuhaPAg',
    'winstonjoulu': 'CAADBAADQAADlS56CC-y3uHoyBk9Ag',
    'pusheenwinston': 'CAADBAADKAADlS56CLUIxcv8o91KAg',
    'penelope': 'CAADBAADKgADlS56CJ0fGrSNoQ_mAg',
    'pingviinigang': 'CAADBAADKwADlS56CLo6nNJF-9kuAg',
    'inttinalle': 'CAADBAADKQADlS56CE8pASMtZ-jqAg',
    'kisuli': 'CAADBAADXwADlS56CL7r1G64m5GQAg',
    'pingviini': 'CAADBAADYAADlS56CNYIEUXgh5upAg'
}


updater = Updater(token)
jq = updater.job_queue

jq.run_repeating(cat_gets_hungry, interval=cat_hungry_random(), first=0)
#updater.dispatcher.add_handler(CommandHandler('hello', hello_world))
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler('koiranalka', dog_hungry))
updater.dispatcher.add_handler(CommandHandler('kisulinalka', cat_hungry))
updater.dispatcher.add_handler(CommandHandler('syotakisuli', feed_cat))
updater.dispatcher.add_handler(CommandHandler('syottokerrat', cat_fed_times))
updater.dispatcher.add_handler(MessageHandler(Filters.all, handle_message))
updater.start_polling()
updater.idle()
