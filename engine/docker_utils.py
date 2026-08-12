import docker
import os


def docker_run(image_name, command=None, workdir=None, user=None, **kwargs):
    client = docker.from_env()
    d = {}
    if command:
        d['command'] = command
    if workdir:
        d['working_dir'] = '/workspace'
        d['volumes'] = [f'{workdir}:/workspace']
    if user:
        d['user'] = user
    else:
        d['user'] = f'{os.getuid()}:{os.getgid()}'
    # d.update(kwargs)
    container = client.containers.run(image=image_name, **d)
    return container.id


def docker_rm(container_id):
    client = docker.from_env()
    client.containers.get(container_id).remove(force=True)


def docker_logs(container_id):
    client = docker.from_env()
    return client.containers.get(container_id).logs().decode('utf-8')
