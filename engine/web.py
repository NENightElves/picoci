import flask
import threading

trigger_list = []
trigger_lock = threading.Lock()
app = flask.Flask(__name__)


def create_trigger(trigger_name):
    with trigger_lock:
        trigger_list.append(trigger_name)


@app.route('/trigger/{name}')
def trigger(name):
    if name in trigger_list:
        ...
    return 'ok'
