# picoci

## Installation
### Docker
1. Build with command `docker build -t picoci .`
2. Run with command
```bash
docker run -d --name picoci -p 5000:5000 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v $(pwd)/yamls:/app/yamls picoci
```
Your `*.yaml` and `*.sec` should be placed in `$(pwd)/yamls`.

## Usage
Put `*.yaml` and `*.sec` into `engine/yamls`, and `cd engine`, run `main.py`.
