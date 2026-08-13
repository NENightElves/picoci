import yaml
import os
import threading
import uuid
from web import create_trigger
from steps import Steps
from logger import Logger


class Task:
    def __init__(self, taskpath):
        if not os.path.exists('tasks'):
            os.makedirs('tasks')
        self.taskpath = taskpath
        self.name = os.path.basename(taskpath)
        self.name, _ = os.path.splitext(self.name)
        self.taskdir = os.path.realpath("tasks/"+self.name)
        self.logs_dir = os.path.realpath("logs/"+self.name)
        if not os.path.exists(self.taskdir):
            os.makedirs(self.taskdir)
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)
        self.j = self.parse_yaml()
        self.logger = Logger(self.name, self.logs_dir)
        self.set_triggers()
        self.steps = None
        self.set_steps()

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
        self.steps = Steps(j, self.taskdir, self.logger)

    def run(self):
        self.logger.reset()
        steps_id = str(uuid.uuid4())
        self.steps.set_step_id(steps_id)
        self.steps.run()
        self.logger.write()

    def stop(self):
        self.steps.stop()

    def reset(self):
        self.steps.reset()

    def __str__(self):
        s = ''
        s += f'Task(name = {self.name}, taskpath = {self.taskpath})\n'
        s += f'  Triggers: {self.j["triggers"]}\n'
        s += '  '+'\n  '.join(str(self.steps).split('\n'))
        return s


class Tasks:

    def __init__(self, tasksdir):
        self.tasksdir = tasksdir
        self.tasks = {}
        self.running_tasks = {}
        self.load()

    def load(self):
        for taskpath in os.listdir(self.tasksdir):
            if taskpath.endswith('.yaml'):
                task = Task(os.path.join(self.tasksdir, taskpath))
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
