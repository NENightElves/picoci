import threading
import os

trigger_dict = {}
trigger_lock = threading.Lock()
l_container_writer = threading.Lock()
tasks = None


def get_data_dir(d=None):
    dd = os.environ.get('PICOCI_DATA_DIR', '/picoci/data')
    if d is None:
        return dd
    return os.path.join(dd, d)


def get_real_data_dir(d=None):
    dd = os.environ.get('PICOCI_REAL_DATA_DIR', '/picoci/data')
    if d is None:
        return dd
    return os.path.join(dd, d)


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


def log_container_list():
    if not os.path.exists('.containers'):
        return []
    with l_container_writer:
        x = []
        with open('.containers', 'r') as f:
            t = f.read()
            if t != '':
                x = t.split('\n')
        return x


def create_trigger(trigger_name, trigger_token=''):
    with trigger_lock:
        trigger_dict[trigger_name] = trigger_token


def check_trigger(trigger_name, trigger_token):
    if trigger_name in trigger_dict and trigger_token == trigger_dict[trigger_name]:
        return True
    return False


def set_tasks(t):
    global tasks
    tasks = t


def get_tasks():
    return tasks
