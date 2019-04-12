# -*- coding: utf-8 -*-
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import os, subprocess
import logging
import random
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
dogIsHungry = False
complainedRecently = True
fedTime = time.time()  # alussa ruokittu


def catFed():  # retrievaa kuinka monta kertaa on syötetty
    try:
        fedFile = open('fedLog.txt', 'r+')
        fedFile.seek(0)  # aina streamin alkuun, sillä spaghettikoodi
        newestFed = int(fedFile.readlines()[-1].split()[1])  # spaghettikoodi
        fedFile.close()  # turvallinen save
    except: # creates the log file with feed_cat()
        newestFed = 0
    return newestFed


def start(bot, update):
    chat_id = update.message.chat.id
    bot.sendMessage(chat_id,
                    'Heissulivei! Tämä on PehmoleluBotti,  jolla voi esim. ruokkia kisulia.')


def exit_handler():
    print("Sammutetaan...")


def cat_hungry(bot, update):
    print(update)  # log that stuff
    chat_id = update.message.chat.id
    global catIsHungry
    if catIsHungry:
        ran = ['Kisuli on nälkäinen! *miaaaaau*',
               'Kisuli on nälkäinen. *murrr*',
               'Kisuli tahtoo ruokaa  /ᐠ｡‸｡ᐟ\\']
        bot.send_photo(chat_id, photo=open('tahtooNamusia.jpg', 'rb'))
    else:
        ran = ["Kummasti kisuli ei ole nälkäinen!",
               "Kisulilla ei maha murise!",
               "Kummasti kisuli ei ole nälkäinen!"]
        bot.sendSticker(chat_id, sticker_map.get('kisuli'))
    bot.sendMessage(chat_id, random.choice(ran))


def cat_hungry_random():  # random aika väliltä
    arvo = random.randint(3*60*60, 6*60*60) # 3h<t<6h
    update_plot() # samalla päivitä plotti
    return arvo


def eaten_recently():
    print('cat has eaten_recently')
    global fedTime
    if fedTime - time.time() > -(2*60*60):    # jos kulunut alle 2h
        return True
    else:
        return False


def cat_gets_hungry():  # muuttaa vaan variablen
    chat_id = -1001291373279
    global catIsHungry, updater
    catIsHungry = True
    if not eaten_recently():
        updater.dispatcher.bot.send_photo(chat_id, photo=open('murr.jpg', 'rb'))
        ran = ['*MIAAAAAAAU* Kisuli ei ole syönyt johonkin aikaan, kisulilla on nälkä!',
               '*murrrrrrrr* Kisulilla on nälkä /ᐠ｡‸｡ᐟ\\',
               'Kisuli tahtoo ruokaa  /ᐠ｡‸｡ᐟ\\']
    else:
        updater.dispatcher.bot.send_photo(chat_id, photo=open('tahtooNamusia.jpg', 'rb'))
        ran = ['Kisuli on nälkäinen! *miaaaaau*',
                'Kisuli on nälkäinen. *murrr*',
                'Kisuli tahtoo ruokaa  /ᐠ｡‸｡ᐟ\\']
    updater.dispatcher.bot.sendMessage(chat_id, random.choice(ran))



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
        '''
        commonWords = list(set(words).intersection(foodWords))
        if commonWords:  # tee tämä hienommaksi
            cat_gets_hungry()
            ruokaSana = random.choice(commonWords)
            ran = ['Kisuli kuulee sanan ' + ruokaSana + ', hän on nyt nälkäinen.',
                   'Kisuli tuli nälkäiseksi kuullessaan sanan ' + ruokaSana,
                   'Kisulille tuli näläkä kuultuaan sanan ' + ruokaSana]
            bot.sendMessage(chat_id, random.choice(ran))
        el'''
        if (not eaten_recently()) and catIsHungry and (not complainedRecently):
            complainedRecently = True
            #bot.sendSticker(chat_id, sticker_map.get('kisuli'))
            bot.send_photo(chat_id, photo=open('murr.jpg', 'rb'))
            ran = ['*MIAAAAAAAU* Kisuli ei ole syönyt johonkin aikaan, kisulilla on nälkä!',
                   '*murrrrrrrr* Kisulilla on nälkä /ᐠ｡‸｡ᐟ\\',
                   'Kisuli tahtoo ruokaa  /ᐠ｡‸｡ᐟ\\']
            bot.sendMessage(chat_id, random.choice(ran))

        if "forceupdateplot" in words:  # debuggaus
            update_plot()

        if "debugsana" in words:  # debuggaus
            bot.sendMessage(chat_id, str(jq._queue))

        # tutkitaan jokaiselle sanalle löytyykö matchia
        for hotword, sticker in sticker_map.items():
            # lähettää stickkerin matchaaviin sanoihin
            if hotword in words:
                bot.sendSticker(chat_id, sticker)


def show_plot(bot, update):
    chat_id = update.message.chat.id
    bot.send_photo(chat_id, photo=open('plotti.png', 'rb'))


# stickerit listana
sticker_map = {
    'koira': 'CAADBAADHQADlS56CMNshytcGo3hAg',
    'winston': 'CAADBAADIQADlS56CKuKJ27vuhaPAg',
    'winstonjoulu': 'CAADBAADQAADlS56CC-y3uHoyBk9Ag',
    'pusheenwinston': 'CAADBAADKAADlS56CLUIxcv8o91KAg',
    'penelope': 'CAADBAADKgADlS56CJ0fGrSNoQ_mAg',
    'pingviinigang': 'CAADBAADKwADlS56CLo6nNJF-9kuAg',
    'inttinalle': 'CAADBAADKQADlS56CE8pASMtZ-jqAg',
    'kisuli': 'CAADBAADXwADlS56CL7r1G64m5GQAg',
    'pingviini': 'CAADBAADYAADlS56CNYIEUXgh5upAg',
    'miisa':'CAADBAADYgADlS56CKRNpGh4NEIKAg'
}


def update_plot():
    # kutsu ./runPlot.run
    subprocess.call("./runPlot.run", shell=True) # selvitä onko turvallisempaa tapaa

def not_complained_recently():
    global complainedRecently
    complainedRecently = False


# ruokasanat
foodWords = [line.rstrip('\n') for line in open("ruokasanat.txt", "r")]

updater = Updater(token)

#   Taustalla menevät prosessit job queuella
jq = updater.job_queue
jq.run_repeating(cat_gets_hungry, interval=cat_hungry_random(), first=0)
jq.run_repeating(not_complained_recently, interval=(0.5*60*60), first=0)
jq.run_repeating(update_plot, interval=(15*60), first=0)
jq.start()

#   Telegram komennot käytäntöön
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('kisulinalka', cat_hungry))
updater.dispatcher.add_handler(CommandHandler('syotakisuli', feed_cat))
#updater.dispatcher.add_handler(CommandHandler('syottokerrat', cat_fed_times))
updater.dispatcher.add_handler(CommandHandler('syottokerrat', show_plot))
updater.dispatcher.add_handler(MessageHandler(Filters.all, handle_message))
updater.start_polling()
updater.idle()

# yritä sulkea fedFile sulkiessa
atexit.register(exit_handler)
