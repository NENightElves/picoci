import logging
import json

logger = logging.getLogger('picoci')


class Logger:

    def __init__(self, name, logs_dir):
        self.name = name
        self.dir = logs_dir

        self.logs = []
        self.task_log = []
        self.steps_log = []
        self.steps = []
        self.container_log = {}
        self.steps_id = ''

    def log_task(self, message):
        self.task_log.append(message)
        self.logs.append(message)
        logger.info(message)

    def log_steps(self, message):
        self.steps_log.append(message)
        self.logs.append(message)
        logger.info(message)

    def log_container(self, container_id, message):
        if container_id not in self.container_log:
            self.container_log[container_id] = []
        self.container_log[container_id].append(message)
        self.logs.append(message)
        logger.info(message)

    def set_steps_id(self, steps_id):
        self.steps_id = steps_id

    def write(self):
        d = {
            'name': self.name,
            'steps_id': self.steps_id,
            'steps': self.steps,
            'container_log': self.container_log
        }
        with open(self.dir + '/' + self.steps_id + '.log', 'w') as f:
            f.write(json.dumps(d))

    def reset(self):
        self.logs = []
        self.task_log = []
        self.steps_log = []
        self.steps = []
        self.container_log = {}
        self.steps_id = ''
