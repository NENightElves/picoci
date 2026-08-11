import docker


def docker_run(image_name, command=None, workdir=None, **kwargs):
    client = docker.from_env()
    d = {}
    d['detach'] = False
    if command:
        d['command'] = command
    if workdir:
        d['working_dir'] = '/workspace'
        d['volumes'] = [f'{workdir}:/workspace']
    d.update(kwargs)
    container = client.containers.run(image=image_name, **d)
    return container


def docker_rm(container_id):
    client = docker.from_env()
    client.containers.get(container_id).remove(force=True)
