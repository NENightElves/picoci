from utils import create_tasks
from web import app as web


def run_web(port=5000):
    web.run(host='0.0.0.0', port=port)


def main():
    create_tasks()
    run_web()


if __name__ == "__main__":
    main()
