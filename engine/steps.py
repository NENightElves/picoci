import docker_utils
import os
from datetime import datetime


class Step:

    def __init__(self, j, taskdir, logger):
        self.logger = logger
        self.name = j['name']
        self.logger.set_step_id(self.name)
        self.status = ''
        self.step = StepContainer(j, taskdir, logger)

    def run(self):
        self.status = 'running'
        self.step.run()
        self.status = self.step.get_status()

    def stop(self):
        self.step.stop()
        self.status = 'stopped'

    def reset(self):
        self.step.reset()
        self.status = ''

    def isReady(self):
        return self.status != 'running'

    def get_status(self):
        return self.status

    def __str__(self):
        return f"Step(name = {self.name}, executor = {self.step})"


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
        self.f_stop = False

    def get(self, index):
        return self.steps[index]

    def run(self):
        self.status = 'running'
        self.logger.log_steps(str(datetime.now())+'\t'+self.status)
        self.progress = f'0/{len(self.steps)}'
        self.logger.log_steps(str(datetime.now())+'\t'+self.progress)
        for i, _ in enumerate(self.steps):
            if self.f_stop:
                self.status = 'stopped'
                self.logger.log_steps(str(datetime.now())+'\t'+self.status)
                break
            _.run()
            self.progress = f'{i+1}/{len(self.steps)}'
            self.logger.log_steps(str(datetime.now())+'\t'+self.progress)
        self.status = 'completed'
        for _ in self.steps:
            if _.status != 'completed':
                self.status = 'failed'
                break
        self.logger.log_steps(str(datetime.now())+'\t'+self.status)

    def stop(self):
        self.f_stop = True

    def reset(self):
        for _ in self.steps:
            _.reset()
        self.status = ''
        self.progress = ''
        self.f_stop = False

    def isReady(self):
        return self.status != 'running'

    def get_status(self):
        return self.status

    def get_progress(self):
        return self.progress

    def set_step_id(self, step_id):
        self.step_id = step_id
        self.logger.set_steps_id(step_id)

    def __str__(self):
        steps = []
        for i, _ in enumerate(self.steps):
            steps.append(str(i)+': '+str(_))
        return f'Steps(taskdir = {self.taskdir})\n  '+'\n  '.join(steps)


class StepContainer:

    def __init__(self, j, taskdir, logger):
        self.logger = logger
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

        self.status = ''
        self.container_id = ''

    def run(self):
        self.status = 'running'
        container_id = docker_utils.docker_run(self.image, self.command, self.workdir)
        for _ in docker_utils.docker_logs_stream(container_id):
            t = _.decode('utf-8')
            if t.endswith('\n'):
                t = t[:-1]
            self.logger.log_step(t)
        status = docker_utils.docker_get_exit_code(container_id)
        docker_utils.docker_rm(container_id)
        if self.status != 'stopped':
            if status == 0:
                self.status = 'completed'
            else:
                self.status = 'failed'

    def stop(self):
        self.status = 'stopped'
        docker_utils.docker_stop(self.container_id)

    def reset(self):
        if self.container_id and docker_utils.docker_is_container_exist(self.container_id):
            docker_utils.docker_rm(self.container_id)
        self.status = ''
        self.container_id = ''

    def get_status(self):
        return self.status

    def __str__(self):
        d = {
            'image': self.image,
            'command': self.command.replace('\n', '\\n'),
            'workdir': self.workdir
        }
        return f"StepContainer({', '.join(f'{k}={v}' for k, v in d.items())})"
