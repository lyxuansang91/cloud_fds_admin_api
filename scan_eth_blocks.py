from datetime import datetime
import time

from web3 import Web3  # noqa
from web3.auto import w3  # noqa
from web3.middleware import geth_poa_middleware  # noqa

from app import models as m  # noqa
from manage import app as a


is_running = True


def init():
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)


def get_latest_block():
    return w3.eth.blockNumber


def process_withdrawal(block_number, block_hash, tx_hash, from_address, to_address, output_index, amount):
    user_address = m.UserAddress.objects(address=from_address).first()
    if user_address is None:
        return
    user_transaction = m.UserTransaction.objects(txHash=tx_hash, transactionType='withdrawal').first()
    if user_transaction:
        return
    print(f'found withdrawal transaction at height: #{block_number}, address: #{from_address}, amount: #{amount}')
    user_transaction = m.UserTransaction(
        userId=user_address.userId,
        fromAddress=from_address,
        fromCurrency='ETH',
        toAddress=to_address,
        toCurrency='ETH',
        amount=amount,
        updatedAt=datetime.utcnow(),
        txHash=tx_hash,
        outputIndex=output_index,
        transactionType='withdrawal')
    user_transaction.save()


def process_deposit(block_number, block_hash, tx_hash, from_address, to_address, output_index, amount):
    user_address = m.UserAddress.objects(address=to_address).first()
    if user_address is None:
        return
    user_transaction = m.UserTransaction.objects(txHash=tx_hash, transactionType='deposit').first()
    if user_transaction:
        return
    print(f'found deposit transaction at height: #{block_number}, address: #{to_address}, amount: #{amount}')
    user_transaction = m.UserTransaction(
        userId=user_address.userId,
        fromAddress=from_address,
        fromCurrency='ETH',
        toAddress=to_address,
        toCurrency='ETH',
        amount=amount,
        updatedAt=datetime.utcnow(),
        txHash=tx_hash,
        outputIndex=output_index,
        transactionType='deposit')
    user_transaction.save()


def process_transaction(transaction):
    tx_hash = transaction['hash'].hex()
    block_number = transaction['blockNumber']
    from_address = transaction['from']
    to_address = transaction['to']
    block_hash = transaction['blockHash'].hex()
    output_index = transaction['transactionIndex']
    amount = Web3.fromWei(transaction['value'], 'ether')
    # process withrdrawal
    process_withdrawal(block_number, block_hash, tx_hash, from_address, to_address, output_index, amount)
    # process deposit
    process_deposit(block_number, block_hash, tx_hash, from_address, to_address, output_index, amount)
    block = m.Block.get_current_block('ETH')
    block.height = int(block_number)
    block.save()


def process_block(index_block):
    global is_running
    try:
        block_info = w3.eth.getBlock(index_block)
    except Exception:
        print(f'error on parse block #{index_block}')
        is_running = False

    for tx_info in block_info.transactions:
        tx_hash = tx_info.hex()  # transaction hash
        transaction = w3.eth.getTransaction(tx_hash)  # get info transaction hash
        process_transaction(transaction)


def main():
    global is_running
    init()
    with a.app_context():
        while is_running:
            current_block = m.Block.get_current_block("ETH")
            latest_block = get_latest_block() - 2
            print(f'current_block: #{current_block.height}, latest block: #{latest_block}')
            current_height = current_block.height
            for index_block in range(current_height, latest_block + 1):
                print(f'ETH: processing block #{index_block}')
                process_block(index_block)
            time.sleep(10)


if __name__ == "__main__":
    main()
