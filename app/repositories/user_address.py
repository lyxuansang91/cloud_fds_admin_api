from app import models as m


class UserAddressRepository(object):
    def get_by_address(self, currency, address):
        return m.UserAddress.objects(currency=currency, address=address).first()._data


user_address_repo = UserAddressRepository()
