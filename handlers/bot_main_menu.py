import time, uuid, requests
from wallet_functions import *
from utils import *
from data import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

def main_menu(update, context):
    user_telegram_id = str(update.effective_user.id)
    request = requests.get(url=f"http://127.0.0.1:5000/addresses/{user_telegram_id}")
    address = request.json()[0]
    private = request.json()[1]
    eth_balance = getBalance(address)
    user_query = update.callback_query

    user = context.user_data

    user["user_address"] = address
    user["user_private"] = private
    if not user_query:
        connector.connect()
        cursor.execute("SELECT telegram_id from users")
        users = str(cursor.fetchall())
        user["input"] = 0
        user["page"] = 0

        if user_telegram_id not in str(users):
            print(user_telegram_id)
            requests.post(
                url="http://localhost:5000/users",
                json={
                    "telegram_id": int(user_telegram_id),
                    "user_quid": str(uuid.uuid1()),
                },
            )
            new_wallet = createWallet()
            requests.post(
                url="http://localhost:5000/addresses",
                json={
                    "telegram_id": int(user_telegram_id),
                    "address": new_wallet[1],
                    "private_key": new_wallet[3],
                },
            )
    # тут есть проблема: пользователя переносит в это меню при вводе данных
    if not (user_query or user["input"]) or user_query.data == "6":
        print('input', user['input'])
        user["input"] = 0
        user["address"] = None
        user["amount"] = None
        wallet_menu = [
            [
                InlineKeyboardButton(buttons[1], callback_data="2"),
                InlineKeyboardButton(buttons[2], callback_data="3"),
            ],
            [InlineKeyboardButton(buttons[4], callback_data="tx_s")],
        ]
        reply_markup = InlineKeyboardMarkup(wallet_menu)
        if user_query:
            context.bot.delete_message(
                chat_id=update.effective_message.chat.id,
                message_id=user_query.message.message_id,
            )
        msg = context.bot.send_message(
            chat_id=update.effective_message.chat.id,
            text="*💰 My Wallet*\n\n" + "*ETH*: " + str(eth_balance) + "\n",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )
        user["message_id"] = msg.message_id
    elif user_query.data == "2":
        print('input2', user['input'])
        user["amount"] = None
        user["address"] = None
        if getBalance(address) != 0:
            user["input"] = 1
            back3 = [[InlineKeyboardButton(buttons[3], callback_data="6")]]
            reply_markup = InlineKeyboardMarkup(back3)
            context.bot.delete_message(
                chat_id=update.effective_message.chat.id,
                message_id=user["message_id"],
            )
            time.sleep(0.5)
            msg = context.bot.send_message(
                chat_id=update.effective_message.chat.id,
                text="*Транзакция (ETH)*\n\nВведите адрес получателя",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup,
            )
            user["message_id"] = msg.message_id

        else:
            back = [[InlineKeyboardButton(buttons[3], callback_data="6")]]
            reply_markup = InlineKeyboardMarkup(back)
            context.bot.delete_message(
                chat_id=update.effective_message.chat.id,
                message_id=user["message_id"],
            )
            time.sleep(0.5)
            msg = context.bot.send_message(
                chat_id=update.effective_message.chat.id,
                text="У вас нет средств на счете, пополните баланс кошелека",
                reply_markup=reply_markup,
            )
            user["message_id"] = msg.message_id
    elif user_query.data == "tx":
        transaction_dict = Transaction(
            user["address"],
            float(user["amount"]),
            user["user_private"],
            user["user_address"],
        )
        context.bot.delete_message(
            chat_id=update.effective_message.chat.id,
            message_id=user["message_id"],
        )
        time.sleep(0.5)
        back = [[InlineKeyboardButton(buttons[3], callback_data="6")]]
        reply_markup = InlineKeyboardMarkup(back)
        msg = context.bot.send_message(
            chat_id=update.effective_message.chat.id,
            text="*Хэш транзакции*\n\n" + "`" + str(transaction_dict[0]) + "`",
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=reply_markup,
        )
        user["message_id"] = msg.message_id
        tx_hash = transaction_dict[0]
        tx_gas = transaction_dict[2]
        gas_price = transaction_dict[4]

        requests.post(
            url="http://127.0.0.1:5000/transactions",
            json={
                "telegram_id": user_telegram_id,
                "to": user["address"],
                "from": user["user_address"],
                "type": "Withdraw",
                "amount": str(user["amount"]) + " ETH",
                "transaction_hash": tx_hash,
                "gasPrice": tx_gas,
            },
        )

    elif user_query.data == "3":
        back1 = [[InlineKeyboardButton(buttons[3], callback_data="6")]]
        reply_markup = InlineKeyboardMarkup(back1)
        context.bot.delete_message(
            chat_id=update.effective_message.chat.id,
            message_id=user["message_id"],
        )
        time.sleep(0.5)
        msg = context.bot.send_message(
            chat_id=update.effective_message.chat.id,
            text="Ваш адрес Ethereum кошелька:\n" + "`" + address + "`",
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=reply_markup,
        )
        user["message_id"] = msg.message_id

    elif (
        user_query.data == "tx_s"
        or user_query.data == "n" + str(user["page"])
        or user_query.data == "prv" + str(user["page"])
    ):
        if user_query.data == "n" + str(user["page"]):
            user["page"] = user["page"] + 1

        if user_query.data == "prv" + str(user["page"]):
            user["page"] = user["page"] - 1

        tx_data = get_tx(str(update.effective_user.id))
        num_pg = tx_data[1]
        all_transactions_of_user = tx_data[0]

        if len(all_transactions_of_user) == 0:
            context.bot.delete_message(
                chat_id=update.effective_message.chat.id,
                message_id=user["message_id"],
            )
            time.sleep(0.5)
            context.bot.send_message(
                chat_id=update.effective_message.chat.id,
                text="У вас нет транзакций ",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(buttons[3], callback_data="6")]]
                ),
            )

        else:

            context.bot.delete_message(
                chat_id=update.effective_message.chat.id,
                message_id=user_query.message.message_id,
            )

            time.sleep(0.5)
            page = "\n".join(all_transactions_of_user[user["page"]])
            page = (
                "стр. "
                + str(user["page"] + 1)
                + "\\"
                + str(num_pg)
                + "\n\n"
                + page
                + "\n"
                + "стр. "
                + str(user["page"] + 1)
                + "\\"
                + str(num_pg)
            )
            if user["page"] == 0 and num_pg == 1:

                msg = context.bot.send_message(
                    chat_id=update.effective_message.chat.id,
                    text=str(page),
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton(buttons[3], callback_data="6")],
                        ]
                    ),
                )
            elif user["page"] + 1 == num_pg:
                msg = context.bot.send_message(
                    chat_id=update.effective_message.chat.id,
                    text=str(page),
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Prev", callback_data="prv" + str(user["page"])
                                )
                            ],
                            [InlineKeyboardButton(buttons[3], callback_data="6")],
                        ]
                    ),
                )
                user["message_id"] = msg.message_id

            elif user["page"] == 0 and num_pg != 1:
                msg = context.bot.send_message(
                    chat_id=update.effective_message.chat.id,
                    text=str(page),
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Next", callback_data="n" + str(user["page"])
                                )
                            ],
                            [InlineKeyboardButton(buttons[3], callback_data="6")],
                        ]
                    ),
                )

                user["message_id"] = msg.message_id
            elif user["page"] != 0 and user["page"] != num_pg - 1:
                msg = context.bot.send_message(
                    chat_id=update.effective_message.chat.id,
                    text=str(page),
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Next", callback_data="n" + str(user["page"])
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    "Prev", callback_data="prv" + str(user["page"])
                                )
                            ],
                            [InlineKeyboardButton(buttons[3], callback_data="6")],
                        ]
                    ),
                )
                user["message_id"] = msg.message_id

