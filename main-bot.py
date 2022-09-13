# sorry for the lack of comments, i wanted to host this on pythonanywhere so.. cant really use # and extra lines. might host it with github with pyscript? idk
# that is why everything is in 1 file too. super bad practice but makes it simple to run.

# pip install python-telegram-bot, telegram-bot
# from constants import API_KEY
import telegram.ext
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, ReplyKeyboardRemove
import datetime
import requests
import jokeapi
import asyncio
import random

API_KEY = '5250260308:AAGbtvCGHuBZ72elNZ-xECuISkPUTuIPgqk'
mode = ''
game_type = ''
td_option = ''


def notify(update, context):
    dt = str(update['message']['date'])[:19]
    hour = str(int(dt[11:13]) + 8) if int(dt[11:13]) < 16 else '0' + str(int(dt[11:13]) - 16)
    sg_dt = dt[:11] + hour + dt[13:] + ' (GMT+8)'
    context.bot.send_message(chat_id=391364421,
                             text=f"First name: {update['message']['chat']['first_name']}\nLast name: {update['message']['chat']['last_name']}\nID: {update['message']['chat']['id']}\nDate: {sg_dt}\nText: {update['message']['text']}")


def start_command(update, context):
    notify(update, context)
    global mode
    global game_type
    global td_option
    mode, game_type, td_option = '', '', ''
    context.bot.send_message(chat_id=update.effective_chat.id, text='Enter a command to get started',
                             reply_markup=ReplyKeyboardRemove(True))
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Command list is available on the bottom left side of your screen')


def get_command(update, context):
    notify(update, context)
    global mode
    global game_type
    global td_option
    mode, game_type, td_option = '', '', ''
    context.bot.send_message(chat_id=update.effective_chat.id, text='''What would you like to get?
    
1. Current datetime
2. Internation Space Station(ISS) current coordinates
3. Joke
4. Cat fact
''', reply_markup=ReplyKeyboardMarkup(
        [[KeyboardButton('Current datetime')], [KeyboardButton('ISS Coordinates')], [KeyboardButton('Joke')],
         [KeyboardButton('Cat fact')], [KeyboardButton('Back')]]))
    mode = 'get'


def game_command(update, context):
    notify(update, context)
    global mode
    global game_type
    global td_option
    mode, game_type, td_option = '', '', ''
    context.bot.send_message(chat_id=update.effective_chat.id, text='''What would you like to play?
    
1. Truth or Dare
2. Would you rather
3. Never have I ever
4. Paranoia
5. Kings cup''', reply_markup=ReplyKeyboardMarkup(
        [[KeyboardButton('Truth or Dare')], [KeyboardButton('Would you rather')], [KeyboardButton('Never have I ever')],
         [KeyboardButton('Paranoia')], [KeyboardButton("King's cup")], [KeyboardButton('Back')]]))
    mode = 'game'


def call_handle_message(update, context):
    asyncio.run(handle_message(update, context))


async def handle_message(update, context):
    notify(update, context)
    global mode
    global game_type
    global td_option
    user_msg = update.message.text.lower()
    match mode:
        case 'get':
            match user_msg:
                case 'back':
                    mode = ''
                    context.bot.send_message(chat_id=update.effective_chat.id, text='Returning..',
                                             reply_markup=ReplyKeyboardRemove(True))
                    start_command(update, context)
                case 'current datetime':
                    current_datetime = datetime.datetime.now()
                    context.bot.send_message(chat_id=update.effective_chat.id, text=str(current_datetime))
                case 'iss coordinates':
                    iss_coord = requests.get('http://api.open-notify.org/iss-now.json').json()
                    context.bot.send_message(chat_id=update.effective_chat.id,
                                             text=f"Longitude: {iss_coord['iss_position']['longitude']}\nLatitude: {iss_coord['iss_position']['latitude']}")
                case 'joke':
                    j = await jokeapi.Jokes()
                    joke = await j.get_joke()
                    if joke["type"] == "single":
                        context.bot.send_message(chat_id=update.effective_chat.id, text=joke["joke"])
                    else:
                        context.bot.send_message(chat_id=update.effective_chat.id, text=joke["setup"])
                        context.bot.send_message(chat_id=update.effective_chat.id, text=joke["delivery"])
                case 'cat fact':
                    response = requests.get('https://cat-fact.herokuapp.com/facts').json()
                    rand = random.randint(0, len(response))
                    context.bot.send_message(chat_id=update.effective_chat.id, text=response[rand]['text'])
                case _:
                    context.bot.send_message(chat_id=update.effective_chat.id,
                                             text="I could not understand your request. Please try again.")
        case 'game':
            match game_type:
                case 'truth or dare':
                    match user_msg:
                        case 't' | 'truth':
                            truth = requests.get('https://api.truthordarebot.xyz/v1/truth').json()['question']
                            context.bot.send_message(chat_id=update.effective_chat.id, text=truth)
                        case 'd' | 'dare':
                            dare = requests.get('https://api.truthordarebot.xyz/api/dare').json()['question']
                            context.bot.send_message(chat_id=update.effective_chat.id, text=dare)
                        case 'back':
                            context.bot.send_message(chat_id=update.effective_chat.id, text='Returning..',
                                                     reply_markup=ReplyKeyboardRemove(True))
                            game_command(update, context)
                case 'would you rather':
                    match user_msg:
                        case 'start' | 'next':
                            msg = requests.get('https://api.truthordarebot.xyz/api/wyr').json()['question']
                            context.bot.send_message(chat_id=update.effective_chat.id,
                                                     text=msg,
                                                     reply_markup=ReplyKeyboardMarkup(
                                                         [[KeyboardButton('Next')],
                                                          [KeyboardButton('Back')]]))
                        case 'back':
                            context.bot.send_message(chat_id=update.effective_chat.id, text='Returning..',
                                                     reply_markup=ReplyKeyboardRemove(True))
                            game_command(update, context)
                case 'never have i ever':
                    match user_msg:
                        case 'start' | 'next':
                            msg = requests.get('https://api.truthordarebot.xyz/api/nhie').json()['question']
                            context.bot.send_message(chat_id=update.effective_chat.id,
                                                     text=msg,
                                                     reply_markup=ReplyKeyboardMarkup(
                                                         [[KeyboardButton('Next')],
                                                          [KeyboardButton('Back')]]))
                        case 'back':
                            context.bot.send_message(chat_id=update.effective_chat.id, text='Returning..',
                                                     reply_markup=ReplyKeyboardRemove(True))
                            game_command(update, context)
                case 'paranoia':
                    match user_msg:
                        case 'start' | 'next':
                            msg = requests.get('https://api.truthordarebot.xyz/api/paranoia').json()['question']
                            context.bot.send_message(chat_id=update.effective_chat.id,
                                                     text=msg,
                                                     reply_markup=ReplyKeyboardMarkup(
                                                         [[KeyboardButton('Next')],
                                                          [KeyboardButton('Back')]]))
                        case 'back':
                            context.bot.send_message(chat_id=update.effective_chat.id, text='Returning..',
                                                     reply_markup=ReplyKeyboardRemove(True))
                            game_command(update, context)
                case "king's cup":
                    context.bot.send_message(chat_id=update.effective_chat.id, text='Returning..',
                                             reply_markup=ReplyKeyboardRemove(True))
                # case 'back':
                #     print('A;LDNCALD;CALSD')
                #     context.bot.send_message(chat_id=update.effective_chat.id, text='Returning..',
                #                              reply_markup=ReplyKeyboardRemove(True))
                #     game_command(update, context)
                case _:
                    match user_msg:
                        case 'truth or dare':
                            game_type = 'truth or dare'
                            context.bot.send_message(chat_id=update.effective_chat.id,
                                                     text=f'{update.message.text} selected!',
                                                     reply_markup=ReplyKeyboardMarkup(
                                                         [[KeyboardButton('Truth')], [KeyboardButton('Dare')],
                                                          [KeyboardButton('Back')]]))
                        case 'would you rather':
                            game_type = 'would you rather'
                            context.bot.send_message(chat_id=update.effective_chat.id,
                                                     text=f'{update.message.text} selected!',
                                                     reply_markup=ReplyKeyboardMarkup(
                                                         [[KeyboardButton('Start')],
                                                          [KeyboardButton('Back')]]))
                        case 'never have i ever':
                            game_type = 'never have i ever'
                            context.bot.send_message(chat_id=update.effective_chat.id,
                                                     text=f'{update.message.text} selected!',
                                                     reply_markup=ReplyKeyboardMarkup(
                                                         [[KeyboardButton('Start')],
                                                          [KeyboardButton('Back')]]))
                        case 'paranoia':
                            game_type = 'paranoia'
                            context.bot.send_message(chat_id=update.effective_chat.id,
                                                     text=f'{update.message.text} selected!',
                                                     reply_markup=ReplyKeyboardMarkup(
                                                         [[KeyboardButton('Start')],
                                                          [KeyboardButton('Back')]]))
                        case "king's cup":
                            game_type = 'kings cup'
                            context.bot.send_message(chat_id=update.effective_chat.id,
                                                     text="I'm still working on this one :)")
                        case 'back':
                            context.bot.send_message(chat_id=update.effective_chat.id, text='Returning..',
                                                     reply_markup=ReplyKeyboardRemove(True))
                            start_command(update, context)
                        case _:
                            context.bot.send_message(chat_id=update.effective_chat.id, text='Invalid input!')
                            mode = ''

        case _:
            greetings = ['hi', 'hey', 'hello', 'hiya']
            if user_msg in greetings:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Hello!')
            elif user_msg == 'poop':
                context.bot.send_message(chat_id=update.effective_chat.id, text='Stupid pocari brocolli')
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text='I did not understand you')


def error(update, context):
    context.bot.send_message(chat_id=391364421, text=f'ERROR:\n\nUpdate:\n {update}\n\ncaused error\n\nContext:\n{context.error}')
    print(f'Update {update} caused error {context.error}')


def main():
    print('Bot started..')
    updater = telegram.ext.Updater(API_KEY, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(telegram.ext.CommandHandler('start', start_command))
    dp.add_handler(telegram.ext.CommandHandler('get', get_command))
    dp.add_handler(telegram.ext.CommandHandler('game', game_command))
    dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, call_handle_message))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


main()
