import flask
from flask import request
import threading
from utils import get_tasks

trigger_dict = {}
trigger_lock = threading.Lock()
app = flask.Flask(__name__)


def create_trigger(trigger_name, trigger_token=''):
    with trigger_lock:
        trigger_dict[trigger_name] = trigger_token


@app.route('/trigger/{name}')
def trigger(name):
    if name not in trigger_dict:
        return 'error'
    if trigger_dict[name] != '':
        t = request.headers.get('Authorization')
        if t != trigger_dict[name]:
            return 'error'
    get_tasks().run(name)
    return 'ok'
