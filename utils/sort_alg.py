# функция sort_pages упорядочивает и форматирует данные о всех транзакциях пользователя для каждой страницы истории и
# возвращает список с этими данными.
# max - максимальное кол-во транзакций на одну страницу
# txs - необработанный список транзакций пользователя из базы данных
# pages - пустой список, нужен для сортировки
def sort_pages(max, txs):
    number_of_pages = 0
    pages = []
    # сортировка данных
    for i in range(0, len(txs), max):
        number_of_pages += 1
        pages.append((tuple(reversed(txs[i : i + max]))))

    info_to_format = []
    # форматирование данных для представления пользователю
    for i in range(0, number_of_pages):
        info_to_format.append([])
        for k, j in enumerate(pages[i]):
            t = str(pages[i][k][9]).split(".")[0]
            info_to_format[i].append(
                "\nHash: "
                + "`"
                + str(j[7])
                + "`"
                + "\nAmount: "
                + str(j[6])
                + "\nFrom: "
                + "`"
                + str(j[4])
                + "`"
                + "\nTo: "
                + "`"
                + str(j[3])
                + "`"
                + "\n"
                "Date: "
                + t
                + "\n\n"
                + f"[Etherscan](https://sepolia.etherscan.io/tx/{str(j[7])})"
                + "\n\n"
                + "*"
                + "_________________________________________________________"
                + "*"
            )
    return info_to_format, number_of_pages
