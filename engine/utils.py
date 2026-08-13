import threading
import os
from tasks import Tasks
from web import app as web

l_container_writer = threading.Lock()
tasks = None


def log_container_create(container_id):
    if not os.path.exists('.containers'):
        with open('.containers', 'w') as f:
            pass
    with l_container_writer:
        x = []
        with open('.containers', 'r') as f:
            t = f.read()
            if t != '':
                x = t.split('\n')
        x.append(container_id)
        with open('.containers', 'w') as f:
            f.write('\n'.join(x))


def log_container_remove(container_id):
    if not os.path.exists('.containers'):
        return
    with l_container_writer:
        x = []
        with open('.containers', 'r') as f:
            t = f.read()
            if t != '':
                x = t.split('\n')
        if container_id in x:
            x.remove(container_id)
        with open('.containers', 'w') as f:
            f.write('\n'.join(x))


def create_tasks(yamlsdir):
    global tasks
    if tasks:
        tasks = Tasks(yamlsdir)
    else:
        tasks = Tasks()


def get_tasks():
    return tasks


def run_web(port=5000):
    web.run(host='0.0.0.0', port=port)
