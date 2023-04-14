# UBKG-API

## Requirements
Python 3.5.2+

## Usage
To run the Flask development server open the project in PyCharm and navigate to `/src/app.py` then click the green arrow

Verify it's running

```
curl localhost:8080
```

## Running with Docker

To run the server on a Docker container, please navigate to the `/docker` directory:
### Localhost
You only need to build the image once. After the image is built you can make changes to the source code and restart the container. The changes will be reflected in the container.

### Build the image
```bash
docker-compose -f docker-compose.yml -p ubkg-api build
```

### Start the container
```bash
docker-compose -f docker-compose.yml -p ubkg-api up -d
```

Make changes to the source code then `down` and `start` the container
```bash
docker-compose -f docker-compose.yml -p ubkg-api down
```

```bash
docker-compose -f docker-compose.yml -p ubkg-api up -d
```