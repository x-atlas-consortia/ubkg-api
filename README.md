# UBKG-API

## Requirements
Python 3.5.2+

## Usage
To run the server, please execute the following from the `/src` directory:

```
pip3 install -r requirements.txt
python3 -m app.py
```


To launch the integration tests, use tox:
```
sudo pip install tox
tox
```

## Running with Docker

To run the server on a Docker container, please execute the following from the `/docker` directory:
### Localhost
build
```bash
./docker-development build
```

start
```bash
./docker-development start
```