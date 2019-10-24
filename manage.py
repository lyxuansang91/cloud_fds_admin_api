from flask import g, request
import os
import time
import datetime

from dotenv import load_dotenv
load_dotenv(override=True)

from app import create_app  # noqa
from app.config import configs as config  # noqa


config_name = os.environ.get('FLASK_CONFIG') or 'develop'
config_cls = config[config_name]
application = app = create_app(config_cls)


@app.before_request
def before_request():
    g.start = time.time()


@app.after_request
def log_request(response):
    if request.path == '/favicon.ico':
        return response
    elif request.path.startswith('/static'):
        return response

    now = time.time()
    duration = round(now - g.start, 6)
    timestamp = datetime.datetime.utcnow().strftime("%d/%b/%Y:%H:%M:%S.%f")[:-3]

    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    host = request.host.split(':', 1)[0]
    args = dict(request.args)

    log_params = [
        ('method', request.method),
        ('path', request.path),
        ('status', response.status_code),
        ('duration', '{}ms'.format(duration)),
        ('time', timestamp),
        ('ip', ip),
        ('host', host),
        ('params', args),
    ]

    request_id = request.headers.get('X-Request-ID')
    if request_id:
        log_params.append(('request_id', request_id))

    line = " ".join(["{}={}".format(name, value) for name, value in log_params])

    app.logger.info(line)

    return response
