#!/bin/bash

BACKEND_CONTAINER_NAME=pubpoint-backend-1 # Update as required
docker exec -it $BACKEND_CONTAINER_NAME python3 api/utils/populate_pubs.py

