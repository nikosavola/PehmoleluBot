# -*- coding: utf-8 -*-
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import os
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
catIsHungry=False
dogIsHungry=False
fedTime=time.clock()  # alussa ruokittu
fedFile=open("fedLog.txt", "w+")


def catFed():  # retrievaa kuinka monta kertaa on syötetty
    return int(fedFile.readlines()[-1].split()[2])  # luetaan syöttökerrat


def start(bot, update):
    chat_id=update.message.chat.id
    bot.sendMessage(chat_id,
        'Heissulivei! Tämä on PehmoleluBotti,  jolla voi esim. ruokkia kisulia.')


def exit_handler():
    fedFile.close()


def cat_hungry(bot, update):
    print(update)  # log that shite
    chat_id=update.message.chat.id
    global catIsHungry
    if catIsHungry:
        ran=['Kisuli on nälkäinen! *miaaaaau*',
               'Kisuli on nälkäinen. *murrr*',
               'Kisuli tahtoo ruokaa  /ᐠ｡‸｡ᐟ\\']
    else:
        ran=["Kummasti kisuli ei ole nälkäinen!",
               "Kisulilla ei maha murise!",
               "Kummasti kisuli ei ole nälkäinen!"]
    random.shuffle(ran)
    tekstiCat=ran[0]
    bot.sendSticker(chat_id, sticker_map.get('kisuli'))
    bot.sendMessage(chat_id, tekstiCat)



def cat_hungry_random():  # random aika väliltä
    arvo=random.randint(10800, 28800)
    return arvo  # 3h<t<8h
# jos kulunut alle 3h ruokkimisesta = True


def eaten_recently():
    print('cat has eaten_recently')
    global fedTime
    if fedTime - time.clock() > -(3*60*60):    # jos kulunut alle 3h
        return True
    else:
        return False


def cat_gets_hungry():  # muuttaa vaan variablen
    global catIsHungry
    catIsHungry=True
    return


def feed_cat(bot, update):
    chat_id=update.message.chat.id
    global catIsHungry, fedTime
    fedTime=time.clock()
    if not catIsHungry:
        ran=['Kisuli ei ole nälkäinen, mutta ottaa silti namun =^._.^=',
               'Kisuli popsii namun, vaikka ei ole nälkäinen.',
               'Kisulilla ei ole näläkä; se ei estä syömästä namua.']
    else:  # on hungry
        catIsHungry=False
        ran=['Kisuli syö namun. Ei ole nyt ainakaan nälkäinen!',
               'Kisuli syö iloisesti nälkäänsä. *miaaaaau*',
               'Kisuli popsii namun ahkerasti!']
    fedFile.write(time.clock + " " + (catFed() + 1))
    bot.sendSticker(chat_id, sticker_map.get('kisuli'))
    bot.sendMessage(chat_id, random.choice(ran))


def cat_fed_times(bot, update):
    chat_id=update.message.chat.id
    fedTeksti='Kisulille on annettu namuja ' + str(catFed()) + ' =^._.^='
    bot.sendMessage(chat_id, fedTeksti)


def handle_message(bot, update):
    chat_id=update.message.chat.id

    if update.message.text:
        words=update.message.text.split()
        words=list(map(lambda x: x.lower(), words))
        global catIsHungry
        commonWords=list(set(words).intersection(foodWords))

        if commonWords:  # tee tämä hienommaksi
            cat_gets_hungry()
            ruokaSana = random.choice(commonWords)
            ran=['Kisuli kuulee sanan ' + ruokaSana + ', hän on nyt nälkäinen.',
                   'Kisuli tuli nälkäiseksi kuullessaan sanan ' + ruokaSana,
                   'Kisulille tuli näläkä kuultuaan sanan ' + ruokaSana]
            bot.sendMessage(chat_id, random.choice(ran))

        elif (not eaten_recently()) and catIsHungry:
            bot.sendSticker(chat_id, sticker_map.get('kisuli'))
            ran=['Kisuli ei ole syönyt johonkin aikaan, kisulilla on nälkä!',
                   'Kisuli on nälkäinen. *murrr*',
                   'Kisuli tahtoo ruokaa  /ᐠ｡‸｡ᐟ\\']
            bot.sendMessage(chat_id, random.choice(ran))

        # tutkitaan jokaiselle sanalle löytyykö matchia
        for hotword, sticker in sticker_map.items():
            # lähettää stickkerin matchaaviin sanoihin
            if hotword in words:
                bot.sendSticker(chat_id, sticker)

# stickerit listana
sticker_map={
    'koira': 'CAADBAADHQADlS56CMNshytcGo3hAg',
    'winston': 'CAADBAADIQADlS56CKuKJ27vuhaPAg',
    'winstonjoulu': 'CAADBAADQAADlS56CC-y3uHoyBk9Ag',
    'pusheenwinston': 'CAADBAADKAADlS56CLUIxcv8o91KAg',
    'penelope': 'CAADBAADKgADlS56CJ0fGrSNoQ_mAg',
    'pingviinigang': 'CAADBAADKwADlS56CLo6nNJF-9kuAg',
    'inttinalle': 'CAADBAADKQADlS56CE8pASMtZ-jqAg',
    'kisuli': 'CAADBAADXwADlS56CL7r1G64m5GQAg',
    'pingviini': 'CAADBAADYAADlS56CNYIEUXgh5upAg'
}

# ruokasanat
foodWords = [line.rstrip('\n') for line in open("ruokasanat.txt", "r")]

updater=Updater(token)

#   Taustalla menevät prosessit job queuella
jq=updater.job_queue
jq.run_repeating(cat_gets_hungry, interval=cat_hungry_random(), first=0)

#   Telegram komennot käytäntöön
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('kisulinalka', cat_hungry))
updater.dispatcher.add_handler(CommandHandler('syotakisuli', feed_cat))
updater.dispatcher.add_handler(CommandHandler('syottokerrat', cat_fed_times))
updater.dispatcher.add_handler(MessageHandler(Filters.all, handle_message))
updater.start_polling()
updater.idle()

# yritä sulkea fedFile sulkiessa
atexit.register(exit_handler)
