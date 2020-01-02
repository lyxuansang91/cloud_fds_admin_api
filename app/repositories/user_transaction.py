from app import models as m


class UserTransactionRespository(object):
    def get_average_deposit(self, user_id):
        user_transactions = m.UserTransaction.objects(transactionType='deposit', userId=user_id)
        if len(user_transactions) == 0:
            return 0
        return sum([user_transaction.amount for user_transaction in user_transactions]) / len(user_transactions)

    def get_balance(self, user_id):
        user_transactions = m.UserTransactions.objects(userId=user_id)
        total_withdrawal = sum([user_transaction.amount for user_transaction in user_transactions if user_transaction.transactionType == 'withdrawal'])
        total_deposit = sum([user_transaction.amount for user_transaction in user_transactions if user_transaction.transactionType == 'deposit'])
        return total_deposit - total_withdrawal

    def get_balance_of_address(self, user_id, address):
        deposit_transactions = m.UserTransactions.objects(userId=user_id, fromAddress=address, transactionType='deposit')
        total_deposit = sum([tx.amount for tx in deposit_transactions])
        withdrawal_transactions = m.UserTransactions.objects(userId=user_id, toAddress=address, transactionType='withdrawal')
        total_withdrawal = sum([tx.amount for tx in withdrawal_transactions])
        return total_deposit - total_withdrawal


user_transaction_repo = UserTransactionRespository()
