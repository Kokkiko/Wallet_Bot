import binascii
import time
import secrets
from web3 import Web3
from eth_account import Account

w3 = Web3(
    Web3.HTTPProvider("https://sepolia.infura.io/v3/3bcee2dd963745379f3f90d9ff08025f")
)


def createWallet():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    return "Адрес кошелька:\n", str(acct.address), "\nПриватный ключ:", str(private_key)


def getBalance(wallet):
    balance = w3.eth.get_balance(wallet)
    eth_balance = w3.from_wei(balance, "ether")
    return eth_balance


def Transaction(to, value, priv, From):
    w3.eth.default_account = From
    nonce = w3.eth.get_transaction_count(From, "pending")
    value = int(float(value) * 1000000000000000000)

    estimate = w3.eth.estimate_gas({"to": to, "from": From, "value": value})
    value_in_eth = w3.from_wei(value, "ether")
    trans = {
        "nonce": nonce,
        "to": to,
        "value": value,
        "gas": estimate,
        "gasPrice": w3.eth.gas_price,
    }
    signed_trans = w3.eth.account.sign_transaction(trans, priv)

    a = w3.eth.send_raw_transaction(signed_trans.rawTransaction)
    trans_hash = binascii.hexlify(a)
    trans_hash = "0x" + str(trans_hash).strip("b").strip("'")
    time.sleep(0.5)
    trans_info = w3.eth.get_transaction(a)

    block_num = trans_info["blockNumber"]
    gas_price = trans_info["gasPrice"]
    gas_priceEth = w3.from_wei(gas_price, "ether")

    f = trans_info["from"]

    return trans_hash, block_num, str(gas_priceEth), f, gas_price


# def erc20_token_transfer(
#     user_adrs, private_key, token_sending_address, amount_of_token_to_send
# ):
#     abi = json.loads(
#         """[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"uint256","name":"_initialSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint8","name":"decimals_","type":"uint8"}],"name":"setupDecimals","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]"""
#     )
#     contract = "0x0Bd5F04B456ab34a2aB3e9d556Fe5b3A41A0BC8D"
#     token_contract = w3.eth.contract(contract, abi=abi)
#     dict_transaction = {
#         "chainId": w3.eth.chain_id,
#         "from": user_adrs,
#         "gasPrice": w3.eth.gas_price,
#         "nonce": w3.eth.getTransactionCount(user_adrs),
#     }
#     token = amount_of_token_to_send * 10**6
#     balance_of_token = token_contract.functions.balanceOf(user_adrs).call()
#     transaction = token_contract.functions.transfer(
#         token_sending_address, token
#     ).buildTransaction(dict_transaction)
#     signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
#     txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
#     time.sleep(0.5)
#     tx_info = w3.eth.get_transaction(txn_hash)
#     gas_price = tx_info["gasPrice"]
#     block = tx_info["blockNumber"]
#     return str(txn_hash.hex()), str(gas_price), block
#
# def is_contract(address):
#     result = len(w3.eth.get_code(address))
#     if result == 0:
#         return False
#     else:
#         return True


# def get_token_balance(user_address):
#     abi = json.loads(
#         """[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"uint256","name":"_initialSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint8","name":"decimals_","type":"uint8"}],"name":"setupDecimals","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]"""
#     )
#     contract = "0x0Bd5F04B456ab34a2aB3e9d556Fe5b3A41A0BC8D"
#     token_contract = w3.eth.contract(contract, abi=abi)
#     balance_of_token = token_contract.functions.balanceOf(user_address).call()
#     return (str(int(balance_of_token / 10**6)) + " USDT"), int(
#         balance_of_token / 10**6
#     )
