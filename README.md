# PehmoleluBot

Telegram bot for feeding a virtual plushie cat.

## Features to add
* Convert MATLAB-plot to Pyplot
* Command that shows who fed the cat first with leaderboards
* Create logfile automatically, (a+)-mode ?


## Prerequisities
* Python 2.7.2+ and PIP
* [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot)
```
$ pip install python-telegram-bot
```

### Setup
* Create a bot and API-key with [@BotFather](http://t.me/BotFather)
* Save the API-key in your terminal to an ENV
```
$ export TG_TOKEN=”YourApiKeyHere”
```
* create a fedLog.txt file in the same directory with the values
```
CURRENTUNIXTIME 0
```

### Running the bot
* Favourably in a screen
```
$ screen -S pehmolelubot
$ python pehmolelubot.py
```


## Example messages
* <img src="https://raw.githubusercontent.com/NikoDaGreat/PehmoleluBot/master/murr.jpg" alt="Hungry cat" width="50%" height="50%" />
* <img src="https://i.imgur.com/q8YjhgY.png" alt="Not-hungry cat" width="40%" height="40%" />


## Special thanks
* Aalto University Guild of Physics (especially their coffee machine)
* [kvantti-telegram-bot-example](https://github.com/EinariTuukkanen/kvantti-telegram-bot-example)
