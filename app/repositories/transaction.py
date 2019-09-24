from app.helper import Helper
from app import models as m


class TransactionRepository(object):
    def get_transaction_list(self, args):
        sortable_fields = ['fromAddress', 'fromCurrency', 'toAddress', 'toCurrency', 'senderIp', 'country']
        page = Helper.get_page_from_args(args)
        size = Helper.get_size_from_args(args)
        sort = Helper.get_sort_from_args(args, sortable_fields)
        if sort is not None:
            column = getattr(m.Transaction, sort[0])
            sort_method = '-' if sort[1] == 'desc' else ''
            transactions = m.Transaction.objects.order_by(sort_method + column.name).paginate(page=page, per_page=size)
        return transactions


tran_repo = TransactionRepository()
