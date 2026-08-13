import yaml
import os
import re
import threading
import uuid
from datetime import datetime
from web import create_trigger
from steps import Steps
from logger import Logger


class Task:
    def __init__(self, name, j):
        if not os.path.exists('tasks'):
            os.makedirs('tasks')
        self.name = name
        self.taskdir = os.path.realpath("tasks/"+self.name)
        self.logs_dir = os.path.realpath("logs/"+self.name)
        if not os.path.exists(self.taskdir):
            os.makedirs(self.taskdir)
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)
        self.j = j
        self.logger = Logger(self.name, self.logs_dir)
        self.set_triggers()
        self.steps = None
        self.set_steps()

    def set_triggers(self):
        j = self.j['triggers']
        for _ in j:
            if _['type'] == 'web-trigger':
                t = ''
                if 'token' in _:
                    t = _['token']
                create_trigger(self.name, t)

    def set_steps(self):
        j = self.j['steps']
        self.steps = Steps(j, self.taskdir, self.logger)

    def run(self):
        self.logger.reset()
        steps_id = str(datetime.now()).split('.')[0].replace(' ', '-').replace(':', '-') + '_' + str(uuid.uuid4())
        self.steps.set_step_id(steps_id)
        self.steps.run()
        self.logger.write()

    def stop(self):
        self.steps.stop()

    def reset(self):
        self.steps.reset()

    def __str__(self):
        s = ''
        s += f'Task(name = {self.name}, j = {self.j})\n'
        s += f'  Triggers: {self.j["triggers"]}\n'
        s += '  '+'\n  '.join(str(self.steps).split('\n'))
        return s


class Tasks:

    def __init__(self, yamlsdir='yamls'):
        self.yamlsdir = yamlsdir
        self.tasks = {}
        self.running_tasks = {}
        self.load()

    def load(self):
        for taskpath in os.listdir(self.yamlsdir):
            if taskpath.endswith('.yaml'):
                name = os.path.splitext(taskpath)[0]
                d = {}
                if os.path.exists(os.path.join(self.yamlsdir, f'{name}.sec')):
                    with open(os.path.join(self.yamlsdir, f'{name}.sec'), 'r') as f:
                        t = f.read()
                        for _ in t.split('\n'):
                            if '=' in _:
                                d[_[0:_.index('=')]] = _[_.index('=')+1:]
                content = ''
                with open(os.path.join(self.yamlsdir, f'{name}.yaml'), 'r') as f:
                    content = f.read()
                for k, v in d.items():
                    pattern = r"\{\{\s*" + re.escape(k) + r"\s*\}\}"
                    content = re.sub(pattern, v, content)
                j = yaml.safe_load(content)
                task = Task(name, j)
                self.tasks[task.name] = task

    def run(self, name):
        if name not in self.tasks or name in self.running_tasks:
            return
        t = threading.Thread(target=self.tasks[name].run)
        self.running_tasks[name] = t
        t.start()

    def stop(self, name):
        if name not in self.running_tasks:
            return
        self.tasks[name].stop()
        self.running_tasks[name].join()

    def __str__(self):
        s = []
        for _ in self.tasks.values():
            s.append(str(_))
        return '\n'.join(s)
