#!/bin/bash

# Start nginx in background
# 'daemon off;' is nginx configuration directive
nginx -g 'daemon off;' &

echo "Sleeping for 120 s"
sleep 120
# Start uwsgi and keep it running in foreground.

# Divergence from standard hubmapconsortium API configuration:
# The ubkg-api is compiled as a PyPI package. The src directory has an additional level, with
# subdirectory for the actual API source and the PyPA Egg. The uwsgi.ini is in the ubkg_api
# subdirectory.
uwsgi --ini /usr/src/app/src/ubkg_api/uwsgi.ini