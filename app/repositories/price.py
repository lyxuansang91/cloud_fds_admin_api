from flask import current_app

from app import models as m
from dateutil.parser import parse


class PriceRepository(object):
    def findPrice(self, billingType, invoiceDate):
        try:
            if isinstance(invoiceDate, str):
                invoiceDate = parse(invoiceDate).date()
            billingTypeDoc = m.BillingType.objects.get(id=billingType)
            priceDoc = m.Price.objects(billingType=billingTypeDoc.id, startDate__lte=invoiceDate).order_by('-startDate').first()
            return priceDoc.price
        except Exception as err:
            current_app.logger.error(err)
            return None


price_repo = PriceRepository()
