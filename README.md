# picoci

## Installation
### Docker
1. Build with command `docker build -t picoci .`
2. Run with command
```bash
docker run -d --name picoci -p 5000:5000 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v $(pwd)/yamls:/picoci/yamls \
    -v /picoci/data:/picoci/data \
    -e PICOCI_DATA_DIR=/picoci/data \
    -e PICOCI_REAL_DATA_DIR=/picoci/data \
    picoci
```
Your `*.yaml` and `*.sec` should be placed in `$(pwd)/yamls`.

## Usage
Put `*.yaml` and `*.sec` into `engine/yamls`, and `cd engine`, run `main.py`.
