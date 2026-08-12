import docker_utils
import os


class Step:

    def __init__(self, j, taskdir, logger):
        self.logger = logger
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
        self.status = ''
        self.container_id = ''

    def run(self):
        self.status = 'running'
        container_id = docker_utils.docker_run(self.image, self.command, self.workdir)
        self.logs = docker_utils.docker_logs(container_id)
        status = docker_utils.docker_get_exit_code(container_id)
        docker_utils.docker_rm(container_id)
        if status == 0:
            self.status = 'completed'
        else:
            self.status = 'failed'

    def reset(self):
        if self.container_id:
            docker_utils.docker_rm(self.container_id)
        self.logs = ''
        self.status = ''
        self.container_id = ''

    def isReady(self):
        return self.status != 'running'

    def get_logs(self):
        return self.logs

    def get_status(self):
        return self.status

    def __str__(self):
        d = {
            'name': self.name,
            'image': self.image,
            'command': self.command.replace('\n', '\\n'),
            'workdir': self.workdir
        }
        return f"Step({', '.join(f'{k}={v}' for k, v in d.items())})"


class Steps:

    def __init__(self, j, taskdir, logger):
        self.steps = []
        self.taskdir = taskdir
        self.step_id = ''
        self.logger = logger
        for _ in j:
            self.steps.append(Step(_, taskdir, self.logger))

        self.status = ''
        self.progress = ''

    def get(self, index):
        return self.steps[index]

    def run(self):
        self.status = 'running'
        self.progress = f'0/{len(self.steps)}'
        for i, _ in enumerate(self.steps):
            _.run()
            self.progress = f'{i+1}/{len(self.steps)}'
        self.status = 'completed'
        for _ in self.steps:
            if _.status != 'completed':
                self.status = 'failed'
                break

    def reset(self):
        for _ in self.steps:
            _.reset()
        self.status = ''
        self.progress = ''

    def isReady(self):
        return self.status != 'running'

    def get_status(self):
        return self.status

    def get_progress(self):
        return self.progress

    def set_step_id(self, step_id):
        self.step_id = step_id
        self.logger.set_step_id(step_id)

    def __str__(self):
        steps = []
        for i, _ in enumerate(self.steps):
            steps.append(str(i)+': '+str(_))
        return f'Steps(taskdir = {self.taskdir})\n  '+'\n  '.join(steps)
