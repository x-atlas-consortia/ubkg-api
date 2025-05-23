#!/bin/bash

# Script for calling Docker compose to control the ubkg-front-end services container of UBKGBox.
# This script differs from the docker-deployment.sh script primarily in that it allows for
# building a new image.

# Arguments and functions:
# 1. check
#    Verifies the location of the app.cfg file for ubkg-api that is to be mounted externally.
# 2. config
#    Calls Docker compose config.
# 3. build
#    a. Refreshes ubkg-api source from the current branch. The src directory is copied under
#       the docker directory, and it is this src that the Dockerfile copies to the image.
#    b. Recalculates content of BUILD file in the container from branch information.
#    c. Recalculates content of the VERSION file in the container from the ubkg-api repository.
#       The UBKGBox deployment version will correspond to the version of the ubkg-api.
#    d. Builds a new image.
# 4. start
#    Builds a container from the current image with docker compose up.
# 5. stop, down
#    Executes corresponding docker compose commands on the current container.
# -- Divergence from standard hubmapconsortium API image build
# 6. push
#    Pushes images in both linux/amd64 and linux/arm64 to Docker Hub.
# --


echo
echo "==================== UBKGBox front end ===================="

# The `absent_or_newer` checks if the copied src at docker/some-api/src directory exists 
# and if the source src directory is newer. 
# If both conditions are true `absent_or_newer` writes an error message 
# and causes script to exit with an error code.
function absent_or_newer() {
    if  [ \( -e $1 \) -a \( $2 -nt $1 \) ]; then
        echo "$1 is out of date"
        exit -1
    fi
}

function get_dir_of_this_script() {
    # This function sets DIR to the directory in which this script itself is found.
    # Thank you https://stackoverflow.com/questions/59895/how-to-get-the-source-directory-of-a-bash-script-from-within-the-script-itself
    SCRIPT_SOURCE="${BASH_SOURCE[0]}"
    while [ -h "$SCRIPT_SOURCE" ]; do # resolve $SCRIPT_SOURCE until the file is no longer a symlink
        DIR="$( cd -P "$( dirname "$SCRIPT_SOURCE" )" >/dev/null 2>&1 && pwd )"
        SCRIPT_SOURCE="$(readlink "$SCRIPT_SOURCE")"
        [[ $SCRIPT_SOURCE != /* ]] && SCRIPT_SOURCE="$DIR/$SCRIPT_SOURCE" # if $SCRIPT_SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
    done
    DIR="$( cd -P "$( dirname "$SCRIPT_SOURCE" )" >/dev/null 2>&1 && pwd )"
    echo 'DIR of script:' $DIR
}

# Generate the build version based on git branch name and short commit hash and write into BUILD file
function generate_build_version() {
    GIT_BRANCH_NAME=$(git branch | sed -n -e 's/^\* \(.*\)/\1/p')
    GIT_SHORT_COMMIT_HASH=$(git rev-parse --short HEAD)
    # Clear the old BUILD version and write the new one
    truncate -s 0 ../BUILD
    # Note: echo to file appends newline
    echo $GIT_BRANCH_NAME:$GIT_SHORT_COMMIT_HASH >> ../BUILD
    # Remmove the trailing newline character
    truncate -s -1 ../BUILD

    echo "BUILD(git branch name:short commit hash): $GIT_BRANCH_NAME:$GIT_SHORT_COMMIT_HASH"
}

# Set the version environment variable for the docker build
# Version number is from the VERSION file
# Also remove newlines and leading/trailing slashes if present in that VERSION file
function export_version() {
    export UBKG_API_VERSION=$(tr -d "\n\r" < ../VERSION | xargs)
    echo "UBKG_API_VERSION: $UBKG_API_VERSION"
}


if [[ "$1" != "check" && "$1" != "config" && "$1" != "build" && "$1" != "start" && "$1" != "stop" && "$1" != "down" && "$1" != "push" ]]; then
    echo "Unknown command '$1', specify one of the following: check|config|build|push|start|stop|down"
else
    # Always show the script dir
    get_dir_of_this_script

    # Always export and show the version
    export_version
    
    # Always show the build in case branch changed or new commits
    generate_build_version

    # Print empty line
    echo

    if [ "$1" = "check" ]; then
        # Bash array.
        # Divergence from standard hubmapconsortium API architecture:
        # ubkg-api is compiled as a PyPI package. The src directory has an additional level, with
        # subdirectories for both the actual API source and the PyPA Egg.
        # The path to API source is different.
        config_paths=(
            '../src/ubkg_api/instance/app.cfg'
        )

        for pth in "${config_paths[@]}"; do
            if [ ! -e $pth ]; then
                echo "Missing file (relative path to DIR of script) :$pth"
                exit -1
            fi
        done

        absent_or_newer ubkg-api/src ../src

        echo 'Checks complete, all good :)'
    elif [ "$1" = "config" ]; then
        docker compose -f docker-compose.yml -f docker-compose.development.yml -p ubkg-front-end config
    elif [ "$1" = "build" ]; then
        # Delete the copied source code dir if exists
        if [ -d "ubkg-api/src" ]; then
            rm -rf ubkg-api/src
        fi

        # Copy over the src folder
        cp -r ../src ubkg-api/

        # Delete old VERSION and BUILD files if found
        if [ -f "ubkg-api/VERSION" ]; then
            rm -rf ubkg-api/VERSION
        fi
        
        if [ -f "ubkg-api/BUILD" ]; then
            rm -rf ubkg-api/BUILD
        fi
        
        # Copy over the VERSION and BUILD files
        cp ../VERSION ubkg-api
        cp ../BUILD ubkg-api

        docker compose -f docker-compose.yml -f docker-compose.development.yml -p ubkg-front-end build
    elif [ "$1" = "start" ]; then
        docker compose -f docker-compose.yml -f docker-compose.development.yml -p ubkg-front-end up -d
    elif [ "$1" = "stop" ]; then
        docker compose -f docker-compose.yml -f docker-compose.development.yml -p ubkg-front-end stop
    elif [ "$1" = "down" ]; then
        docker compose -f docker-compose.yml -f docker-compose.development.yml -p ubkg-front-end down
    elif [ "$1" = "push" ]; then
        # buildx uses docker-compose.yml
        docker buildx bake -f docker-compose.yml -f docker-compose.development.yml --push
    fi
fi

