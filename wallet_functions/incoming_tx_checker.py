import requests, binascii
from Wallet_Bot.wallet_functions.FinanceEngine import w3
from Wallet_Bot.data.data_base_connect import cursor


# начало цикла
def check_incoming_tx():
    while 1:
        # извлечение всех имеющихся в базе адресов в кортеж "addresses"
        query = "SELECT address FROM addresses"
        cursor.execute(query)
        addresses = cursor.fetchall()
        users = []
        for i in range(0, len(addresses)):
            a = addresses[i][0]
            users.append(a)

        # block это словарь, который хранит информацию о последнем блоке
        block = w3.eth.get_block("latest")
        # 'transaction_hash' поочередно принимает в себя каждое значение из block['transactions'],
        # ключ 'transactions' - список, в котором находятся все хеши транзакций
        for transaction_hash in block["transactions"]:
            # tx равно конкретной транзакции, найденной по данному хешу
            tx = w3.eth.get_transaction_receipt(transaction_hash)
            print(tx["to"])

            # проверяется, есть ли адрес получателя tx['to'] из данной транзакции в нашем списке адресов
            # если есть, то данная транзакция сохраняется в базу, затем проверяется следующий хеш
            # если нет, то на соответствие этому условию проверяется следующий хеш
            if (tx["to"] in users and tx["from"] != tx["to"]) or tx["from"] in users:
                tx2 = w3.eth.get_transaction(transaction_hash)
                hash = tx["transactionHash"]
                hash = binascii.hexlify(hash)
                transaction_hash = "0x" + str(hash).strip("b").strip("'")
                From = tx["from"]
                to = tx["to"]
                value = w3.from_wei(tx2["value"], "ether")
                gasPrice = w3.from_wei(tx2["gasPrice"], "ether")
                blockNum = tx["blockNumber"]
                print(transaction_hash, From, to, value, gasPrice, blockNum)

                cursor.execute(
                    "SELECT telegram_id FROM addresses WHERE address=%s", str(to)
                )
                query = cursor.fetchone()
                id = query[0]

                # сохранение транзакции в базу
                requests.post(
                    url="http://127.0.0.1:5000/transactions",
                    json={
                        "telegram_id": id,
                        "to": to,
                        "from": From,
                        "type": "Deposit",
                        "amount": str(float(value)) + " ETH",
                        "transaction_hash": transaction_hash,
                        "gasPrice": str(gasPrice),
                    },
                )
