from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, ReplyKeyboardRemove, Bot, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import asyncio
import logging
import requests
import json
from random import randint
from copy import deepcopy
from constants import OWNER_ID, API_KEY

'''
Config
'''
ENDPOINT = 'https://game-telegram-bot-gules.vercel.app'

card_types = [
    'A\n\nMe! - You drink!',
    '2\n\nSabotage! - Person on your left drinks!',
    '3\n\nSabotage! - Person on your right drinks!',
    '4\n\nLaw! - Set a rule that will last for the rest of the game. Whoever breaks it drink!',
    '5\n\nMate! - Choose a partner. They will have to drink everytime you drink!',
    '6\n\nCategory! - Choose an item category and go in a anti-clockwise direction with everyone naming a valid item in the category. First to fail drinks!',
    '7\n\n7-UP! - Go clockwise with each person listing a number starting from 1 but you must replace the multiples of 7 with "UP". First to fail drinks!',
    '8\n\nRhyme! - Come up with a word and go anti-clockwise with everybody saying a valid word that rhymes with your word. First to fail drinks!',
    '9\n\nFight! - Rock paper scissors with the person sitting opposite you. Loser drinks!',
    '10\n\nBreak! - Everyone gets to use the toilet!',
    'J\n\nDicks! - Guys drink!',
    'Q\n\nWhores! - Girls drink!',
    "K\n\nRoyal chef! - Add an edible item into the king's cup!"
]
kCard = "K\n\nRoyal chef! - Add an edible item into the king's cup!"

allCards = deepcopy(card_types)*4


class User:
    def __init__(self, mode='', gameMode='', cards=deepcopy(allCards)) -> None:
        self.mode = mode
        self.gameMode = gameMode
        self.cards = cards
        self.prevCard = None


validGamemodes = ['truth or dare',
                  'never have i ever', 'paranoia', "king's cup"]


activeUsers = {
    391364421: User(),
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
    activeUsers[userId].gameMode = ''
    await context.bot.send_message(chat_id=update.effective_chat.id, text='What would you like to get?', reply_markup=ReplyKeyboardMarkup([
        [KeyboardButton('DateTime')],
        [KeyboardButton('Joke')],
        [KeyboardButton('Pickup Line')],
        [KeyboardButton('Back')],
    ]))


async def gameCommandHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    userId = update.effective_chat.id
    activeUsers[userId].mode = 'game'
    activeUsers[userId].gameMode = ''
    await context.bot.send_message(chat_id=update.effective_chat.id, text='What would you like to play?', reply_markup=ReplyKeyboardMarkup([
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
        if msg == 'datetime':
            data = json.loads(requests.get(
                ENDPOINT + '/datetime').text)['data']
            await context.bot.send_message(chat_id=userId, text=data)
            return
        elif msg == 'joke':
            await context.bot.send_message(chat_id=userId, text='You :]')
            return
        elif msg == 'pickup line':
            await context.bot.send_message(chat_id=userId, text='On a scale of 1-10, you are a 9 and I am the 1 you need ;]')
            return
        elif msg == 'back':
            await startCommandHandler(update, context)
            return

    elif user.mode == 'game':
        if user.gameMode == '':
            if msg in validGamemodes:
                if msg == 'truth or dare':
                    await context.bot.send_message(userId, text=f'You have selected {update.message.text}. Select truth or dare to begin!', reply_markup=ReplyKeyboardMarkup([
                        [KeyboardButton('Truth')],
                        [KeyboardButton('Dare')],
                        [KeyboardButton('Back')],
                    ]))
                    return

                await context.bot.send_message(userId, text=f'You have selected {update.message.text}. Tap on `Hit` to begin!', reply_markup=ReplyKeyboardMarkup([
                    [KeyboardButton('Hit')],
                    [KeyboardButton('Back')],
                ]))

                if msg == "king's cup":
                    await context.bot.sendMessage(userId, text='\n\n'.join(card_types))

                user.gameMode = msg
                user.cards = deepcopy(allCards)
            elif msg == 'back':
                await startCommandHandler(update, context)
                return
            else:
                await context.bot.send_message(userId, "I couldn't understand you, please try a little harder!")
            return

        elif user.gameMode == 'truth or dare':
            if msg == 'truth':
                path = '/game/tod/t'
            elif msg == 'dare':
                path = '/game/tod/d'
            elif msg == 'back':
                await gameCommandHandler(update, context)
                return
            data = json.loads(requests.get(ENDPOINT + path).text)['data']
            await context.bot.sendMessage(userId, data)
            return

        elif user.gameMode == 'never have i ever' or user.gameMode == 'paranoia':
            if msg == 'hit':
                data = json.loads(requests.get(
                    ENDPOINT + ('/game/nhie' if user.gameMode == 'never have i ever' else '/game/paranoia')).text)['data']
                await context.bot.sendMessage(userId, data)
            elif msg == 'back':
                await gameCommandHandler(update, context)
            return

        elif user.gameMode == "king's cup":
            if msg == 'hit':
                if len(user.cards) == 0:
                    await context.bot.sendMessage(userId, "You are out of cards! Press back and select King's cup to reset the deck and play again.")
                    return
                if kCard not in user.cards:
                    await context.bot.sendMessage(userId, "All kings are out! The last person who drew the King's card has to eat/drink the King's cup!\n\nPress back and select King's cup to reset the deck and play again.")

                randNum = randint(0, len(user.cards)-1)
                while user.prevCard == user.cards[randNum]:
                    randNum = randint(0, len(user.cards)-1)

                card = user.cards[randNum]
                user.prevCard = card
                user.cards.pop(randNum)
                await context.bot.sendMessage(userId, card)
            elif msg == 'back':
                await gameCommandHandler(update, context)
            return


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
