from Wallet_Bot.handlers.bot_handler import updater
from Wallet_Bot.wallet_functions.incoming_tx_checker import check_incoming_tx
from Wallet_Bot.data.crud import app


def main():
    updater.start_polling()
    app.run(debug=False)
    check_incoming_tx()


if __name__ == "__main__":
    main()
 