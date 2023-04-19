from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, ReplyKeyboardRemove, Bot, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import asyncio
import logging
import requests

'''
Config
'''

OWNER_ID = 391364421
API_KEY = '5250260308:AAGbtvCGHuBZ72elNZ-xECuISkPUTuIPgqk'

allCards = '123456789TJQK'*4

activeUsers = {
    391364421: {'mode': '', 'gameMode': '', 'cards': allCards},
}
'''
mode: None/get/game
gameMode: None,kc (king's cup)
'''

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


'''
global useful functions
'''


async def notify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''
    notifies bot owner when someone is using the bot
    '''
    # print(notify.__doc__)

    dt = str(update.message.date)[:19]
    print(dt)
    hour = str(int(dt[11:13]) + 8) if int(dt[11:13]
                                          ) < 16 else '0' + str(int(dt[11:13]) - 16)
    sg_dt = dt[:11] + hour + dt[13:] + ' (GMT+8)'
    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=f"Username: {update.message.chat.username}\n\
First name: {update.message.chat.first_name}\n\
Last name: {update.message.chat.last_name}\n\
ID: {update.message.chat.id}\nDate: {sg_dt}\n\
Text: {update.message.text}"
    )


'''
Command handlers
'''


async def startCommandHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await notify(update, context)

    await context.bot.send_message(chat_id=update.effective_chat.id, text='Enter a command to get started',
                                   reply_markup=ReplyKeyboardRemove(True))
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Command list is available on the bottom left side of your screen',
                                   reply_markup=ReplyKeyboardMarkup([
                                       # [KeyboardButton('/start')],
                                       [KeyboardButton('/get')],
                                       [KeyboardButton('/game')],
                                       [KeyboardButton('/help')]
                                   ])
                                   )


async def getCommandHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    userId = update.effective_chat.id
    activeUsers[userId].mode = 'get'
    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=ReplyKeyboardMarkup([
        [KeyboardButton('DateTime')],
        [KeyboardButton('Joke')],
        [KeyboardButton('Pickup Line')],
        [KeyboardButton('Back')],
    ]))


async def gameCommandHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    userId = update.effective_chat.id
    activeUsers[userId].mode = 'game'
    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=ReplyKeyboardMarkup([
        [KeyboardButton('Truth or Dare')],
        [KeyboardButton('Never have I ever')],
        [KeyboardButton('Paranoia')],
        [KeyboardButton("King's cup")],
        [KeyboardButton('Back')],
    ]))


async def helpCommandHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(update.effective_chat.id, "You're smart, I'm sure you'll figure it out ;D")


'''
Error handler
'''


def errorHandler(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="An exception has occurred!\n\nPlease inform the bot owner about this issue and the steps that caused it.")
    context.bot.send_message(chat_id=OWNER_ID,
                             text=f'ERROR:\n\nUpdate:\n {update}\n\ncaused error\n\nContext:\n{context.error}')
    print(f'Update {update} caused error {context.error}')


'''
Message handler
'''


async def messageHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await notify(update, context)

    msg = update.message.text.lower()
    userId = update.effective_chat.id
    user = activeUsers[userId]

    if user.mode == 'get':


def main():
    app = ApplicationBuilder().token(API_KEY).build()

    app.add_error_handler(errorHandler)
    app.add_handler(CommandHandler('start', startCommandHandler))
    app.add_handler(CommandHandler('get', getCommandHandler))
    app.add_handler(CommandHandler('game', gameCommandHandler))
    app.add_handler(CommandHandler('help', helpCommandHandler))
    app.add_handler(MessageHandler(
        filters.TEXT & (~filters.COMMAND), messageHandler))  # bitwise operators

    app.run_polling()


if __name__ == '__main__':
    main()
