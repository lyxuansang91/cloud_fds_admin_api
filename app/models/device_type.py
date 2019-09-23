from app.extensions import db


class DeviceType(db.Document):
    deviceId = db.IntField(required=True)
    deviceType = db.StringField(required=True, max_length=50)

    meta = {'collection': 'deviceType'}

    @db.queryset_manager
    def objects(doc_cls, queryset):
        return queryset.order_by('deviceId')
