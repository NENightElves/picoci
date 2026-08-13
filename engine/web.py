import flask
from flask import request
import threading
from utils import get_tasks, check_trigger


app = flask.Flask(__name__)


@app.route('/trigger/{name}')
def trigger(name):
    t = request.headers.get('Authorization', '')
    if check_trigger(name, t) == False:
        return 'error'
    get_tasks().run(name)
    return 'ok'
