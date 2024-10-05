from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Updater,
    Filters,
    CallbackQueryHandler,
)

# from Wallet_Bot.handlers.bot_start_menu import start
from handlers.bot_main_menu import main_menu
from handlers.bot_menu2 import menu_handler_2


TOKEN = "6539624111:AAGKngaVGJaMkAFL0MSa0u_rrhI9dw1kUIM"
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

main_handler = MessageHandler(Filters.all, main_menu)
second_handler = MessageHandler(Filters.text, menu_handler_2)

dispatcher.add_handler(main_handler)
dispatcher.add_handler(second_handler)

dispatcher.add_handler(CallbackQueryHandler(main_menu))
dispatcher.add_handler(CallbackQueryHandler(menu_handler_2))
