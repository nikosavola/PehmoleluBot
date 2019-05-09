# PehmoleluBot

Telegram bot for feeding a virtual plushie cat.

## Features to add
* Convert MATLAB-plot to Pyplot
* Make the food words hasten the time it takes for the cat to get hungry
  * Random chance of rendering the cat hungry upon hearing a food word. Preferably with a cooldown.


## Prerequisities
* Python 2.7.2+ and PIP
* MATLAB R2016b or newer
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


### Running the bot
* Favourably in a screen
```
$ screen -S pehmolelubot
$ python pehmolelubot.py
```


## Example messages
* <img src="https://raw.githubusercontent.com/NikoDaGreat/PehmoleluBot/master/murr.jpg" alt="Hungry cat" width="50%" height="50%" />
* <img src="https://i.imgur.com/q8YjhgY.png" alt="Non-hungry cat" width="40%" height="40%" />
* <img src="https://i.imgur.com/y72Jo7g.png" alt="Non-hungry cat" width="60%" height="60%"/>

## Special thanks
* Aalto University Guild of Physics (especially their coffee machine)
* [kvantti-telegram-bot-example](https://github.com/EinariTuukkanen/kvantti-telegram-bot-example)
