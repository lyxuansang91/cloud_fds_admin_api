from flask import current_app
from app import models as m


class UserChangeBillingTypeRepository(object):
    def insert_one(self, args):
        try:
            change_billing_type = m.UserChangeBillingType(**args)
            change_billing_type.save()
            return change_billing_type
        except Exception as ex:
            current_app.logger.error(ex)
            return None


user_change_billing_type_repo = UserChangeBillingTypeRepository()
