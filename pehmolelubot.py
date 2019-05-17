# -*- coding: utf-8 -*-
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import os
import subprocess
import logging
import random
import numpy
import datetime
import time
import atexit

logging.basicConfig(
    filename='spam.log',
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s'
)

#   telegram API-key
token = os.environ['TG_TOKEN']

########  globaalit variablet ########
catIsHungry = False
complainedRecently = True
fedTime = time.time()  # alussa ruokittu
foodWordsHeard = 0 # alustetaan laskuri


def start(bot, update):
    chat_id = update.message.chat.id
    bot.sendMessage(chat_id,
                    'Heissulivei! Tämä on PehmoleluBotti,  jolla voi esim. ruokkia kisulia.')


def exit_handler():
    print("Sammutetaan...")


def catFed():  # retrievaa kuinka monta kertaa on syötetty
    try:
        fedFile = open('fedLog.txt', 'r+')
        fedFile.seek(0)  # aina streamin alkuun, sillä spaghettikoodi
        newestFed = int(fedFile.readlines()[-1].split()[1])  # spaghettikoodi
        fedFile.close()  # turvallinen save
    except:  # creates the log file with feed_cat()
        newestFed = 0
    return newestFed


def cat_hungry(bot, update):
    print(update)  # log that stuff
    chat_id = update.message.chat.id
    global catIsHungry
    if catIsHungry:
        ran = ['Kisuli on nälkäinen! *miaaaaau*',
               'Kisuli on nälkäinen. *murrr*',
               'Kisuli tahtoo ruokaa  /ᐠ｡‸｡ᐟ\\']
        bot.send_photo(chat_id, photo=open('Images/tahtooNamusia.jpg', 'rb'))
    else:
        ran = ["Kummasti kisuli ei ole nälkäinen!",
               "Kisulilla ei maha murise!",
               "Kummasti kisuli ei ole nälkäinen!"]
        bot.sendSticker(chat_id, sticker_map.get('kisuli'))
    bot.sendMessage(chat_id, random.choice(ran))


def cat_hungry_random():  # random aika
    # return random.randint(3*60*60, 6*60*60) # 3h<t<6h
    global foodWordsHeard
    nextTime = 0
    while (nextTime < 60*15):
        nextTime = numpy.random.exponential(1.5)*4*60*60 - numpy.random.exponential(3.0)* foodWordsHeard * 60
    foodWordsHeard = 0
    return nextTime


def eaten_recently():
    print('cat has eaten_recently')
    global fedTime
    if fedTime - time.time() > -(2*60*60):    # jos kulunut alle 2h
        return True
    else:
        return False


def cat_gets_hungry(bot=None, job=None):  # muuttaa vaan variablen
    chat_id = [-1001291373279] # -1001131311658
    global catIsHungry, updater
    catIsHungry = True
    if not eaten_recently():
        for id in chat_id:
            updater.dispatcher.bot.send_photo(id, photo=open('Images/murr.jpg', 'rb'))
        ran = ['*MIAAAAAAAU* Kisuli ei ole syönyt johonkin aikaan, kisulilla on nälkä!',
               '*murrrrrrrr* Kisulilla on nälkä /ᐠ｡‸｡ᐟ\\',
               'Kisuli tahtoo ruokaa  /ᐠ｡‸｡ᐟ\\']
    else:
        for id in chat_id:
            updater.dispatcher.bot.send_photo(id, photo=open('Images/tahtooNamusia.jpg', 'rb'))
        ran = ['Kisuli on nälkäinen! *miaaaaau*',
               'Kisuli on nälkäinen. *murrr*',
               'Kisuli tahtoo ruokaa  /ᐠ｡‸｡ᐟ\\']
    for id in chat_id:
        updater.dispatcher.bot.sendMessage(id, random.choice(ran))
    jq.run_once(cat_gets_hungry, when=cat_hungry_random())  # stack the new time for feeding


def feed_cat(bot, update):
    chat_id = update.message.chat.id
    global catIsHungry, fedTime, complainedRecently
    fedTime = time.time()
    complainedRecently = False
    if not catIsHungry:
        ran = ['Kisuli ei ole nälkäinen, mutta ottaa silti namun =^._.^=',
               'Kisuli popsii namun, vaikka ei ole nälkäinen.',
               'Kisulilla ei ole näläkä; se ei estä syömästä namua.']
    else:  # on hungry
        catIsHungry = False
        ran = ['Kisuli syö namun. Ei ole nyt ainakaan nälkäinen!',
               'Kisuli syö iloisesti nälkäänsä. *miaaaaau*',
               'Kisuli popsii namun ahkerasti!']
        add_point(bot, update)  # lisää piste jos nälkäsyöttö
    nowFed = catFed() + 1
    fedFile = open('fedLog.txt', 'a+')
    fedFile.write(str(time.time()) + " " + str(nowFed) + "\n")
    fedFile.close()
    bot.sendSticker(chat_id, sticker_map.get('kisuli'))
    bot.sendMessage(chat_id, random.choice(ran))


def cat_fed_times(bot, update):
    chat_id = update.message.chat.id
    fedTeksti = 'Kisulille on annettu namuja ' + str(catFed()) + ' =^._.^='
    bot.sendMessage(chat_id, fedTeksti)


def handle_message(bot, update):
    chat_id = update.message.chat.id
    if update.message.text:
        words = update.message.text.split()
        words = list(map(lambda x: x.lower(), words))
        global catIsHungry, complainedRecently
        commonWords = list(set(words).intersection(foodWords))

        if commonWords:  # tee tämä hienommaksi
            '''
            global catIsHungry
            catIsHungry = True  '''
            ruokaSana = random.choice(commonWords)
            '''
            ran = ['Kisuli kuulee sanan ' + ruokaSana + ', hän on nyt nälkäinen.',
                   'Kisuli tuli nälkäiseksi kuullessaan sanan ' + ruokaSana,
                   'Kisulille tuli näläkä kuultuaan sanan ' + ruokaSana]    '''
            ran = ['Kisuli kuulee sanan ' + ruokaSana + ', hän melkein tuli nälkäiseksi.',
                   'Kisuli ei aivan nälkääntynyt kuullessaan sanan ' + ruokaSana,
                   'Kisulille tuli melkein näläkä kuultuaan sanan ' + ruokaSana
            foodWordsHeard += 1
            bot.sendMessage(chat_id, random.choice(ran))

        elif (not eaten_recently()) and catIsHungry and (not complainedRecently):
            complainedRecently = True
            bot.send_photo(chat_id, photo=open('Images/murr.jpg', 'rb'))
            ran = ['*MIAAAAAAAU* Kisuli ei ole syönyt johonkin aikaan, kisulilla on nälkä!',
                   '*murrrrrrrr* Kisulilla on nälkä /ᐠ｡‸｡ᐟ\\',
                   'Kisuli tahtoo ruokaa  /ᐠ｡‸｡ᐟ\\']
            bot.sendMessage(chat_id, random.choice(ran))

        if "forceupdateplot" in words:  # debuggaus
            update_plot()
        # tutkitaan jokaiselle sanalle löytyykö matchia
        for hotword, sticker in sticker_map.items():
            # lähettää stickkerin matchaaviin sanoihin
            if hotword in words:
                bot.sendSticker(chat_id, sticker)


def show_plot(bot, update):
    chat_id = update.message.chat.id
    bot.send_photo(chat_id, photo=open('plotti.png', 'rb'))


def show_leaderboards(bot, update):
    chat_id = update.message.chat.id
    bot.send_photo(chat_id, photo=open('leaderboards.png', 'rb'))


def add_point(bot, update):
    pointsFile = open('leaderboardsLog.txt', 'a+')
    pointsFile.write(str(time.time()) + " " + str(update.message.from_user.username) + "\n")
    pointsFile.close()


"""
def wappu(bot, update):
    chat_id = update.message.chat.id
    bot.send_photo(chat_id, photo=open('Images/wappu.png', 'rb'))
"""

# stickerit listana
sticker_map = {
    'husky-strawberry': 'CAADBAADHQADlS56CMNshytcGo3hAg',
    'winston': 'CAADBAADIQADlS56CKuKJ27vuhaPAg',
    'winstonjoulu': 'CAADBAADQAADlS56CC-y3uHoyBk9Ag',
    'pusheenwinston': 'CAADBAADKAADlS56CLUIxcv8o91KAg',
    'penelope': 'CAADBAADKgADlS56CJ0fGrSNoQ_mAg',
    'pingviinigang': 'CAADBAADKwADlS56CLo6nNJF-9kuAg',
    'inttinalle': 'CAADBAADKQADlS56CE8pASMtZ-jqAg',
    'kisuli': 'CAADBAADXwADlS56CL7r1G64m5GQAg',
    'pingviini': 'CAADBAADYAADlS56CNYIEUXgh5upAg',
    'miisa': 'CAADBAADYgADlS56CKRNpGh4NEIKAg',
    'kaarleppi': 'CAADBAADHgADlS56CIVOivZh0GgWAg',
    'мишка': 'CAADBAADYwADlS56CGH_gl4AAXE1SAI',
}


def update_plot(bot=None, job=None):
    subprocess.call("./runPlot.run", shell=True)  # selvitä onko turvallisempaa tapaa


def not_complained_recently(bot=None, job=None):
    global complainedRecently
    complainedRecently = False


def show_leaderboards_daily(bot=None, job=None):
    chat_id = [-1001291373279, -1001131311658]
    for id in chat_id:
        bot.send_photo(chat_id, photo=open('leaderboards.png', 'rb'))


# ruokasanat kerralla muistiin
foodWords = [line.rstrip('\n') for line in open("ruokasanat.txt", "r")]

updater = Updater(token)


#   Taustalla menevät prosessit job queuella
jq = updater.job_queue
#   jq.run_repeating(cat_gets_hungry, interval=cat_hungry_random(), first=cat_hungry_random())
jq.run_once(cat_gets_hungry, when=cat_hungry_random())  # first run
jq.run_repeating(not_complained_recently, interval=(0.5*60*60), first=0)
jq.run_repeating(update_plot, interval=(30*60), first=0)
jq.run_daily(show_leaderboards_daily, datetime.time.min)  # keskiöittäin

#   Telegram komennot käytäntöön
updater.dispatcher.add_handler(CommandHandler('start', start))
#updater.dispatcher.add_handler(CommandHandler('wappu', wappu))
updater.dispatcher.add_handler(CommandHandler('kisulinalka', cat_hungry))
updater.dispatcher.add_handler(CommandHandler('syotakisuli', feed_cat))
updater.dispatcher.add_handler(CommandHandler('syottokerrat', show_plot))
updater.dispatcher.add_handler(CommandHandler('leaderboards', show_leaderboards))
updater.dispatcher.add_handler(MessageHandler(Filters.all, handle_message))
updater.start_polling()
updater.idle()

# yritä sulkea fedFile sulkiessa
atexit.register(exit_handler)
