#!/bin/bash

# Pass the HOST_UID and HOST_UID from environment variables for exec'ing the
# process in the container.  These values should match those of a user with
# write permission on the mount point for the log directory on the
# host system, but not root.  The mount point is specified in
# docker-compose.yml under services:ubkg-api:volumes:
HOST_GID=${HOST_GID}
HOST_UID=${HOST_UID}
echo "Starting ubkg-api container with the host user UID: $HOST_UID and GID: $HOST_GID"

# Create a new user with the same host UID to run processes on container
# The Filesystem doesn't really care what the user is called,
# it only cares about the UID attached to that user
# Check if user already exists and don't recreate across container restarts
getent passwd $HOST_UID > /dev/null 2&>1
# $? is a special variable that captures the exit status of last task
if [ $? -ne 0 ]; then
    groupadd -g $HOST_GID data-distillary
    useradd -u $HOST_UID -g $HOST_GID -m data-distillary
fi
touch /var/run/nginx.pid
chown -R data-distillary:data-distillary /var/run/nginx.pid
chown -R data-distillary:data-distillary /var/cache/nginx
chown -R data-distillary:data-distillary /var/log/nginx
# Lastly we use gosu to execute our process "$@" as the user above, with
# permissions on all appropriate resources.
# Remember CMD from a Dockerfile of child image gets passed to the entrypoint.sh as command line arguments
# "$@" is a shell variable that means "all the arguments"
exec /usr/local/bin/gosu data-distillary "$@"

