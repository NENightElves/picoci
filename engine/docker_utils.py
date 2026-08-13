import docker
import os
import utils


def docker_run(image_name, command=None, workdir=None, user=None, **kwargs):
    client = docker.from_env()
    d = {}
    d['detach'] = True
    if command:
        d['command'] = command
    if workdir:
        d['working_dir'] = '/workspace'
        d['volumes'] = [f'{workdir}:/workspace']
    if user:
        d['user'] = user
    # d.update(kwargs)
    container = client.containers.create(image=image_name, **d)
    utils.log_container_create(container.id)
    container.start()
    return container.id


def docker_stop(container_id):
    if docker_is_container_exist(container_id):
        client = docker.from_env()
        client.containers.get(container_id).stop()


def docker_rm(container_id):
    client = docker.from_env()
    client.containers.get(container_id).remove(force=True)
    utils.log_container_remove(container_id)


def docker_logs(container_id):
    client = docker.from_env()
    return client.containers.get(container_id).logs().decode('utf-8')


def docker_logs_stream(container_id):
    client = docker.from_env()
    return client.containers.get(container_id).logs(stream=True)


def docker_wait_container(container_id):
    client = docker.from_env()
    return client.containers.get(container_id).wait()


def docker_is_container_exist(container_id):
    client = docker.from_env()
    try:
        client.containers.get(container_id)
        return True
    except docker.errors.NotFound:
        return False


def docker_get_exit_code(container_id):
    client = docker.from_env()
    return client.containers.get(container_id).attrs['State']['ExitCode']


def docker_container_clean():
    client = docker.from_env()
    for _ in utils.log_container_list():
        docker_rm(_)
