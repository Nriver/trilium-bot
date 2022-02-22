import json
import os
import sys
from datetime import datetime
from functools import wraps

import telebot
from loguru import logger
from telebot import apihelper
from telebot import types
from trilium_py.client import ETAPI

from settings import http_proxy, token, admin_list, trilium_server_url, etapi_token

apihelper.proxy = {'https': http_proxy}

bot = telebot.TeleBot(token)


def restricted(func):
    """Access Limit"""

    @wraps(func)
    def wrapped(message, *args, **kwargs):
        # user_id = message.chat.id
        user_id = message.from_user.id
        # Filter user id
        if user_id not in admin_list:
            logger.error(f'Access Denied for user_id: {user_id}')
            return
        return func(message, *args, **kwargs)

    return wrapped


def build_todo_list_markup(todo_list):
    """
    build markup for todo list
    :param todo_list:
    :return:
    """
    markup = types.InlineKeyboardMarkup()
    for i, (status, todo) in enumerate(todo_list):
        if status:
            todo_message = '✅ ' + todo
        else:
            todo_message = '🟩 ' + todo
        markup.add(types.InlineKeyboardButton(text=todo_message,
                                              callback_data=json.dumps({
                                                  'type': 'TODO_toggle',
                                                  'index': i,
                                                  'status': status
                                              })))
    return markup


@bot.message_handler(commands=['id'])
def send_user_id(message):
    """
    return telegram user id
    this function has no access limit
    :param message:
    :return:
    """
    bot.reply_to(message, message.from_user.id)


@bot.message_handler(commands=['start', 'help'])
@restricted
def send_welcome(message):
    # Note: if buttons modified, a new `/start` is required to get the latest buttons.

    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)

    btn_todo = types.KeyboardButton('TODO')
    btn_toggle_quick_add = types.KeyboardButton('Toggle Quick Add')
    btn_restart = types.KeyboardButton('Restart')
    btn_status = types.KeyboardButton('Status')
    btn_id = types.KeyboardButton('ID')
    markup.row(btn_todo, btn_toggle_quick_add)
    markup.row(btn_status, btn_id, btn_restart)
    bot.reply_to(message, "Hi, please choose ~", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    logger.info('callback')
    logger.info(f'{call.data}')
    data = json.loads(call.data)

    if data['type'] == 'TODO_toggle':
        status = data['status']
        ea.todo_check(data['index'], check=not status)
        todo_list = ea.get_todo()
        return bot.send_message(call.message.chat.id, text="Current TODO List",
                                reply_markup=build_todo_list_markup(todo_list))

    return bot.answer_callback_query(call.id, "ok")


@bot.message_handler(func=lambda message: True)
@restricted
def echo_all(message):
    logger.info(f'Receive message')

    msg = message.text

    if msg in ['id', 'ID']:
        return send_user_id(message)
    elif msg in ['Toggle Quick Add', ]:
        config['quick_add'] = not config['quick_add']
        save_config()
        return bot.reply_to(message, f"quick_add {config['quick_add']}")
    elif msg in ['Restart']:
        bot.reply_to(message, f"rebooting...")
        os.execv(sys.executable, ['python'] + sys.argv)
        return
    elif msg in ['Status', ]:
        return bot.reply_to(message, f"Started {str(datetime.now() - begin_time).split('.')[0]}")
    elif msg in ['TODO', ]:
        todo_list = ea.get_todo()
        logger.info(todo_list)
        return bot.reply_to(message, "Current TODO List", reply_markup=build_todo_list_markup(todo_list))

    if config['quick_add']:
        day_note = ea.inbox(datetime.now().strftime("%Y-%m-%d"))
        logger.info(f"day_note {day_note['noteId']}")
        logger.info(msg)
        ea.create_note(
            parentNoteId=day_note['noteId'],
            title="TG message",
            type="text",
            content=msg,
        )
        return bot.reply_to(message, "Added to Trilium")

    return bot.reply_to(message, msg)


def save_config():
    global config
    global config_file
    logger.info(f'save_config')
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(config, ensure_ascii=False, indent=4))


def load_config():
    global config
    global config_file
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.loads(f.read())
    # default configs
    default_config = {
        'quick_add': True,
        'single_note': False,
    }
    for x in default_config:
        if x not in config:
            config[x] = default_config[x]


if __name__ == '__main__':
    begin_time = datetime.now()
    config_file = 'config.json'
    config = {}
    load_config()
    save_config()

    ea = ETAPI(trilium_server_url, etapi_token)
    logger.info(f'{bot.get_me().username} started')
    bot.polling(none_stop=True, timeout=10)
