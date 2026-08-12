import yaml
import os
from web import create_trigger
from steps import Steps


class Task:
    def __init__(self, taskpath):
        if not os.path.exists('tasks'):
            os.makedirs('tasks')
        self.taskpath = taskpath
        self.name = os.path.basename(taskpath)
        self.name, _ = os.path.splitext(self.name)
        self.taskdir = os.path.realpath("tasks/"+self.name)
        if not os.path.exists(self.taskdir):
            os.makedirs(self.taskdir)
        self.j = self.parse_yaml()
        self.set_triggers()
        self.steps = self.set_steps()

    def parse_yaml(self):
        with open(self.taskpath, 'r') as f:
            return yaml.safe_load(f)

    def set_triggers(self):
        j = self.j['triggers']
        for _ in j:
            if _['type'] == 'web-trigger':
                create_trigger(self.name)

    def set_steps(self):
        j = self.j['steps']
        steps = Steps(j, self.taskdir)
        return steps

    def __str__(self):
        s = ''
        s += f'Task(name = {self.name}, taskpath = {self.taskpath})\n'
        s += f'  Triggers: {self.j["triggers"]}\n'
        s += '  '+'\n  '.join(str(self.steps).split('\n'))
        return s
