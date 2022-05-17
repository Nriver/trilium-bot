# trilium-bot

Telegram bot for Trilium Notes powered by Trilium-py.

# What is it?

It's a Telegram Bot to interact with Trilium Notes. Mainly I use it to manage my todo list.

It uses a standard python module named [trilium-py](https://github.com/Nriver/trilium-py) ( which I wrote :) ) to communicate with Trilium through [ETAPI](https://github.com/zadam/trilium/wiki/ETAPI).

# Features

1. Send '/start' to the bot to get feature buttons.

2. Send text messages to the bot, it will save the message as a subnote to today's note.

3. Tapping `TODO List` will get you todo list from today's note. Then tap the item to get it checked/unchecked. Also, you
can add/delete/update todos with the function buttons.

4. The bot contains a scheduled task to automatically move yesterday's unfinished/unchecked todo items to today's note. You
can change the time to execute it in `config.json`.

# How to use

0. Please refer to (official docs)[https://core.telegram.org/bots] to create a bot if you do not have one.
1. Install packages with `pip3 install -r requirements.txt --user`.
2. Open `settings.py` and change the config to yours. Please note that you must set `admin_list` correctly. Only user
   who is in this list can use this bot.
3. Run with `python3 trilium-bot.py`.

# How to update

1. Update code `git pull`
2. Update dependency `pip3 install -U -r requirements.txt --user`
