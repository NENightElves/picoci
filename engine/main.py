from tasks import Tasks
from utils import set_tasks
from web import app as web
import logging


def run_web(port=5000):
    web.run(host='0.0.0.0', port=port)


def main():
    tasks = Tasks()
    set_tasks(tasks)
    run_web()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
