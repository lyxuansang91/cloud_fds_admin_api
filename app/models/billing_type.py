from app.extensions import db


class BillingType(db.Document):
    billingType = db.StringField(required=True, regex=r'^(Free trial|Monthly|Metered)$', unique=True)

    meta = {'collection': 'billingType'}
