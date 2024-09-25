import pymysql

# finance_base_connector = pymysql.connect(host='localhost', user='root',
#                                          password='b269bba3', database='fe')
# finance_base_cursor = finance_base_connector.cursor()

connector = pymysql.connect(host='127.0.0.1', user='root',
                                             password='b269bba3', database='fe')
cursor = connector.cursor()
# connector.ping(reconnect=True)

