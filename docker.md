## Dockerfile

FROM        # base image to start from
WORKDIR     # set working directory inside container
COPY        # copy files from your machine into image
RUN         # run a command during build (install packages)
EXPOSE      # document which port the app uses
CMD         # command to run when container starts

```Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```


## Build Image

```bash
docker build -t <image-name> .
```

### Run the container

```bash
docker run -d -p 5000:5000 --name <container-name> <image-name>
```

### Run the container with volume enabled

```bash
docker run -d -p 5000:5000 --name <container-name> -v ${pwd}/data:/app/data <image-name>
```

---

## docker-compose.yml

```yml
version: '3.8'

services:
  web:
    build: .
    image: flask-app:dev
    container_name: test-app
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
    restart: always
```

### Commands

```bash
# Start everything (builds image if not built yet)
docker-compose up

# Start in background
docker-compose up -d

# Force rebuild image + start (use this when you change code)
docker-compose up -d --build

# Stop everything + remove containers
docker-compose down

# See logs
docker-compose logs

# Live logs (follows output)
docker-compose logs -f
```

---