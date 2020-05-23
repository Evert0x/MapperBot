from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from web3 import Web3
import requests
import settings

def error(update, context, error):
    """Log Errors caused by Updates."""
    pass

def handle_update_message(bot, update):
    if "/start" in update.message.text:
        r = requests.get("%s/get/%s" % (
            settings.MAPPER, update.effective_user.id
        )).json()
        if r["status"]:
            update.message.reply_text("Current address: %s" % r["address"])
        update.message.reply_text("Please give your Ethereum address (0x..)")
    elif Web3.isAddress(update.message.text):
        address = Web3.toChecksumAddress(update.message.text)
        r = requests.get("%s/add/%s/%s" % (
            settings.MAPPER, update.effective_user.id, address
        )).json()
        if r["status"]:
            update.message.reply_text("Address updated to %s" % address)
        else:
            update.message.reply_text("Something went wrong")
    else:
        update.message.reply_text("try /start")

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(settings.BOT_TOKEN)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, handle_update_message))
    dp.add_handler(MessageHandler(Filters.command, handle_update_message))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()