from app import models as m


class WithdrawalRequestRepository(object):
    def create(self, user_id, from_address, to_address, currency, amount, code='0', active=True):
        withdrawal_request = m.WithdrawalRequest(userId=user_id, fromAddress=from_address, toAddress=to_address,
                                                 fromCurrency=currency, amount=amount, toCurrency=currency, code=code, active=active)
        withdrawal_request.save()
        return withdrawal_request._data

    def withdrawal_requests_from_user(self, user_id):
        withdrawal_requests = m.WithdrawalRequest.objects(userId=user_id)
        return [withdrawal_request._data for withdrawal_request in withdrawal_requests]

    def get_withdrawal(self, id):
        withdrawal_request = m.WithdrawalRequest.objects(id=id).first()
        return withdrawal_request

    def approve_request(self, withdrawal_request):
        withdrawal_request.active = True
        withdrawal_request.save()
        return withdrawal_request


withdrawal_request_repo = WithdrawalRequestRepository()
