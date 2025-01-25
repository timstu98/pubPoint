#!/bin/bash

###
# Various useful bash commands I have found. This script is not meant to be run as is
###

# Find the root of the Git repository
REPO_ROOT=$(git rev-parse --show-toplevel)
if [ $? -ne 0 ]; then
    echo "Error: This script must be run inside a Git repository."
    exit 1
fi
# Change to the repository root
cd "$REPO_ROOT" || exit
echo "Changed directory to repository root: $REPO_ROOT"

# Run your commands here
python3 app/backend/api/utils/populate_pubs.py



## A method of running commands within a docker container
docker exec -it $BACKEND_CONTAINER_NAME sh -c "
pwd
python3 api/utils/populate_pubs.py
"