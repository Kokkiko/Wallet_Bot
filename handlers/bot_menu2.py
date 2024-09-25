import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from Wallet_Bot.wallet_functions.FinanceEngine import w3, getBalance


def menu_handler_2(update, context):
    user = context.user_data
    user["address"] = update.message.text
    if user["input"] == 1 and user["address"] == None:
        user["address"] = update.message.text
        validate = w3.is_address(user["address"])
        if validate == True:
            back = [[InlineKeyboardButton("↩️ Back", callback_data="6")]]
            reply_markup = InlineKeyboardMarkup(back)
            context.bot.delete_message(
                chat_id=update.effective_message.chat.id,
                message_id=user["message_id"],
            )
            time.sleep(0.5)
            msg = context.bot.send_message(
                chat_id=update.effective_message.chat.id,
                text=f"*Транзакция ({user['button']})*\n\nВведите сумму",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup,
            )
            user["message_id"] = msg.message_id
        elif validate == False:
            back = [[InlineKeyboardButton("↩️ Back", callback_data="2")]]
            reply_markup = InlineKeyboardMarkup(back)
            print(user)
            context.bot.delete_message(
                chat_id=update.effective_message.chat.id,
                message_id=user["message_id"],
            )
            time.sleep(0.5)
            msg = context.bot.send_message(
                chat_id=update.effective_message.chat.id,
                text="Вы неверно ввели адрес!",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup,
            )
            user["message_id"] = msg.message_id
    if user["input"] == 1 and user["address"] != None:
        user["amount"] = update.message.text
        print(user)
        if getBalance(user["user_address"]) < float(user["amount"]) or getBalance(
            user["user_address"]
        ) == float(user["amount"]):
            back = [[InlineKeyboardButton("↩️ Back", callback_data="2")]]
            reply_markup = InlineKeyboardMarkup(back)
            context.bot.delete_message(
                chat_id=update.effective_message.chat.id,
                message_id=user["message_id"],
            )
            time.sleep(0.5)
            msg = context.bot.send_message(
                chat_id=update.effective_message.chat.id,
                text="У вас не хватает средств на счете!",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup,
            )
            user["message_id"] = msg.message_id
        else:
            tx_menu = [
                [InlineKeyboardButton("Execute Transfer", callback_data="tx")],
                [InlineKeyboardButton("Back", callback_data="2")],
            ]
            reply_markup = InlineKeyboardMarkup(tx_menu)
            context.bot.delete_message(
                chat_id=update.effective_message.chat.id,
                message_id=user["message_id"],
            )
            time.sleep(0.5)
            msg = context.bot.send_message(
                chat_id=update.effective_message.chat_id,
                text="*Транзакция (ETH)*\n\nПодтвердите перевод",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup,
            )
            user["message_id"] = msg.message_id
