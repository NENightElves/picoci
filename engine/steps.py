import docker_utils


class Step:

    def __init__(self, j, taskdir):
        self.name = j['name']
        self.image = j['image']
        if 'commands' in j:
            self.command = 'set -e\n'+'\n'.join(j['commands'])
            self.command = "/bin/sh -c'\n" + self.command + "\n'"
        else:
            self.command = None
        self.workdir = taskdir if 'workdir' not in j else j['workdir']
        if '..' in self.workdir:
            self.workdir = taskdir
        self.workdir = taskdir + '/' + self.workdir

    def run(self):
        docker_utils.docker_run(self.image, self.command, self.workdir)

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

    def __str__(self):
        steps = []
        for i, _ in enumerate(self.steps):
            steps.append(str(i)+': '+str(_))
        return f'Steps(taskdir = {self.taskdir})\n  '+'\n  '.join(steps)
