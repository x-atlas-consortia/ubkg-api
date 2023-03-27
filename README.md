# UBKG-API

## Requirements
Python 3.5.2+

## Usage
To run the Flask development server open the project in PyCharm and navigate to `/src/app.py` then click the green arrow

Verify it's running

```
curl localhost:8080
```


To launch the integration tests, use tox:
```
sudo pip install tox
tox
```

## Running with Docker

To run the server on a Docker container, please navigate to the `/docker` directory:
### Localhost
You only need to build the image once. After the image is built you can make changes to the source code and restart the container. The changes will be reflected in the container.

### Build the image
```bash
./docker-development build
```

### Start the container
```bash
./docker-development start
```

Make changes to the source code then `down` and `start` the container
```bash
./docker-development down
```

```bash
./docker-development start
```