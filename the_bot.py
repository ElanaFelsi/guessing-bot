import logging
from time import sleep

import telegram

import bot_settings
from telegram import InlineKeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters, Updater

logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

updater = Updater(token=bot_settings.BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher


def help(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=f"This game is easy, you need to know some basic rules: \n"
                                                   f"1. Choose a number\n"
                                                   f"2. I'll guess it\n"
                                                   f"3. Just tell me if I should go higher or lower\n"
                                                   f"4. Have FUN!")
    ready_keyboard(update, chat_id, context)


def high_low_keyboard(update, chat_id, context, text):
    ready_menu = [[InlineKeyboardButton('Higher', callback_data='Higher')],
                  [InlineKeyboardButton('Lower', callback_data='Lower')],
                  [InlineKeyboardButton('Yup', callback_data='Yup')]]
    reply_markup = ReplyKeyboardMarkup(ready_menu)
    update.message.reply_text('Choose:', reply_markup=reply_markup)


def guessing_game(update, chat_id, context, text):
    if text == 'Yup':
        context.bot.send_photo(chat_id=chat_id, photo=open('iwin.gif', 'rb'))
        context.user_data['playing'] = False
        reply_markup = telegram.ReplyKeyboardRemove()
        context.bot.send_message(chat_id=chat_id, text="Wanna play again?", reply_markup=reply_markup)
        return
    if context.user_data['start'] == context.user_data['guess'] or context.user_data['end'] == context.user_data['guess']:
        context.bot.send_message(chat_id=chat_id, text=f"No lying allowed\n Is the number {context.user_data['guess']}?")
        context.bot.send_photo(chat_id=chat_id, photo=open('pin.jpg', 'rb'))
        return
    if text != 'Higher' and text != 'Lower':
        context.bot.send_message(chat_id=chat_id, text=f"Is the number {context.user_data['guess']}?")
        return
    else:
        if text == 'Higher':
            context.user_data['start'] = context.user_data['guess']
        elif text == 'Lower':
            context.user_data['end'] = context.user_data['guess']

        context.user_data['guess'] = context.user_data['start'] + (
                    (context.user_data['end'] - context.user_data['start']) // 2)
    context.bot.send_message(chat_id=chat_id, text=f"Is the number {context.user_data['guess']}?")
    high_low_keyboard(update, chat_id, context, text)


def ready_keyboard(update, chat_id, context):
    ready_menu = [[InlineKeyboardButton('Yes', callback_data='Yes')],
                  [InlineKeyboardButton('No', callback_data='No')]]
    reply_markup = ReplyKeyboardMarkup(ready_menu)
    update.message.reply_text('Are you ready?', reply_markup=reply_markup)


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> Start chat #{chat_id}")
    context.user_data['guess'] = 50
    context.user_data['end'] = 100
    context.user_data['start'] = 0
    context.user_data['playing'] = True
    context.user_data['ready'] = False
    context.bot.send_message(chat_id=chat_id, text=f"Hello user, please think of a number from 1-100.")
    sleep(3)
    ready_keyboard(update, chat_id, context)


def ready(update, chat_id, context, text):
    if text == 'Yes':
        high_low_keyboard(update, chat_id, context, text="Choose:")
        guessing_game(update, chat_id, context, text)
        context.user_data['ready'] = True
    else:
        sleep(3)
        ready_keyboard(update, chat_id, context)


def respond(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    text = update.message.text
    logger.info(f"= Got on chat #{chat_id}: {text!r}")
    if not context.user_data['playing']:
        pass
    elif not context.user_data['ready']:
        ready(update, chat_id, context, text)
    else:
        guessing_game(update, chat_id, context, text)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

guess_handler = CommandHandler('guess', start)
dispatcher.add_handler(guess_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

echo_handler = MessageHandler(Filters.text, respond)
dispatcher.add_handler(echo_handler)

logger.info("* Start polling...")
updater.start_polling()  # Starts polling in a background thread.
updater.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")