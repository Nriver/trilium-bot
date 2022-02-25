# trilium-bot

Telegram bot for Trilium Notes powered by Trilium-py.

# What is it?

It's a telegram bot to interact with Trilium Notes.

Send text messages to the bot, it will save the message as a subnote to today's note.

You can get function buttons by sending '/start' to the bot. There are several function. For example,
tapping `TODO List` will get you todo list from today's note. Then tap the item to get it checked/unchecked. Also, you
can add/delete/update todos with the function buttons.

The bot contains a scheduled task to automatically move yesterday's unfinished/unchecked todo items to today's note. You
can change the time to execute it in `config.json`.

# How to use

1. Install packages with `pip3 install -r requirements.txt --user`.
2. Open `settings.py` and change the config to yours. Please note that you must set `admin_list` correctly. Only user
   who is in this list can use this bot.
3. Run with `python3 trilium-bot.py`.

# How to update

1. Update code `git pull`
2. Update dependency `pip3 install -U -r requirements.txt --user`
