from datetime import datetime

from app.extensions import db


class WithdrawalRequest(db.Document):
    userId = db.ObjectIdField()
    fromAddress = db.StringField(required=True, max_length=200)
    toAddress = db.StringField(required=True, max_length=200)
    fromCurrency = db.StringField(required=True, max_length=200)
    toCurrency = db.StringField(required=True, max_length=200)
    amount = db.DecimalField(required=True, precision=10, default=0)
    code = db.StringField(required=True)
    active = db.BooleanField(required=True, default=True)
    createdAt = db.DateTimeField(required=True, default=datetime.utcnow)
    updatedAt = db.DateTimeField()
