import threading
import os

l_container_writer = threading.Lock()


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
