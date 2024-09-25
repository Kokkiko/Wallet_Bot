from Wallet_Bot.utils.sort_alg import sort_pages
from Wallet_Bot.data.data_base_connect import cursor, connector
def get_tx(id):
        print('id',id)
        connector.connect()
        cursor.execute(
            "SELECT * FROM transactions WHERE telegram_id=%s ORDER BY timestamp DESC", id
        )
        connector.close()
        tx_data = sort_pages(10, cursor.fetchall())
        return tx_data[0], tx_data[1]

