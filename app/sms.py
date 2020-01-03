import os  # noqa


def send_sms(to_phone, body):
    from twilio.rest import Client  # noqa
    account_sid = os.environ.get('ACCOUNT_SID')
    auth_token = os.environ.get('AUTH_TOKEN')
    from_ = os.environ.get('FROM_PHONE')
    client = Client(account_sid, auth_token)
    message = client.messages.create(body=body, from_=from_, to=to_phone)
    print(message.sid)
    return message.sid
