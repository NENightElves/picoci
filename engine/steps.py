import docker_utils
import os


class Step:

    def __init__(self, j, taskdir):
        self.name = j['name']
        self.image = j['image']
        if 'commands' in j:
            self.command = 'set -e\n'+'\n'.join(j['commands'])
            self.command = "/bin/sh -c '\n" + self.command + "\n'"
        else:
            self.command = None
        self.workdir = '.' if 'workdir' not in j else j['workdir']
        if '..' in self.workdir:
            self.workdir = '.'
        self.workdir = taskdir + '/' + self.workdir
        self.workdir = os.path.realpath(self.workdir)
        self.logs = ''

    def run(self):
        container_id = docker_utils.docker_run(self.image, self.command, self.workdir)
        self.logs = docker_utils.docker_logs(container_id)

    def __str__(self):
        d = {
            'name': self.name,
            'image': self.image,
            'command': self.command.replace('\n', '\\n'),
            'workdir': self.workdir
        }
        return f"Step({', '.join(f'{k}={v}' for k, v in d.items())})"


class Steps:

    def __init__(self, j, taskdir):
        self.steps = []
        self.taskdir = taskdir
        for _ in j:
            self.steps.append(Step(_, taskdir))

    def get(self, index):
        return self.steps[index]

    def run(self):
        for i, _ in enumerate(self.steps):
            _.run()

    def __str__(self):
        steps = []
        for i, _ in enumerate(self.steps):
            steps.append(str(i)+': '+str(_))
        return f'Steps(taskdir = {self.taskdir})\n  '+'\n  '.join(steps)
